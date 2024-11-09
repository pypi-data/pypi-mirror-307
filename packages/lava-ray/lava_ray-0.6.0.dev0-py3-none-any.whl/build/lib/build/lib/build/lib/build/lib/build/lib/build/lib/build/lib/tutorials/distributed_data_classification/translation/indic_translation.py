import os
import re
from dataclasses import dataclass

import cudf
import dask_cudf
import numpy as np
import torch
import torch.nn as nn
from crossfit import op
from crossfit.backend.torch.hf.model import HFModel
from dask.distributed import get_worker
from nltk.tokenize import sent_tokenize
from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer

from nemo_curator.classifiers.base import DistributedDataClassifier
from nemo_curator.datasets import DocumentDataset
from nemo_curator.utils.distributed_utils import get_client, load_object_on_worker

try:
    from IndicTransToolkit import IndicProcessor
except ModuleNotFoundError:
    raise ImportError(
        "IndicTransToolkit not found. Please install it using the following command: \n"
        + "pip install git+https://github.com/VarunGumma/IndicTransToolkit.git"
    )


@dataclass
class TranslationConfig:
    pretrained_model_name_or_path: str = "ai4bharat/indictrans2-en-indic-1B"
    max_length: int = 50
    num_beams: int = 5
    autocast: bool = False
    max_words_per_sen: int = 200


class CustomModel(nn.Module):
    def __init__(self, config: TranslationConfig):
        super().__init__()
        self.config = config
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            pretrained_model_name_or_path=config.pretrained_model_name_or_path,
            trust_remote_code=True,
        )
        self.autocast = config.autocast

    @torch.no_grad()
    def _forward(self, batch: dict) -> torch.Tensor:
        return self.model.generate(
            **batch,
            use_cache=True,
            min_length=0,
            max_length=self.config.max_length,
            num_beams=self.config.num_beams,
            num_return_sequences=1,
            repetition_penalty=1.2,
        )

    def forward(self, batch: dict) -> torch.Tensor:
        if self.autocast:
            with torch.autocast(device_type="cuda"):
                outputs = self._forward(batch)
        else:
            outputs = self._forward(batch)
        return outputs


class ModelForSeq2SeqModel(HFModel):
    def __init__(self, config: TranslationConfig):
        self.trans_config = config
        self.config = self.load_config()
        super().__init__(self.trans_config.pretrained_model_name_or_path)

    def load_model(self, device: str = "cuda") -> CustomModel:
        model = CustomModel(self.trans_config)
        model = model.to(device)
        model.eval()
        return model

    def load_config(self) -> AutoConfig:
        return AutoConfig.from_pretrained(
            pretrained_model_name_or_path=self.trans_config.pretrained_model_name_or_path,
            trust_remote_code=True,
        )

    def load_tokenizer(self) -> AutoTokenizer:
        return AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.trans_config.pretrained_model_name_or_path,
            trust_remote_code=True,
        )

    def max_seq_length(self) -> int:
        return self.config.max_source_positions

    def load_cfg(self):
        return self.load_config()


def preprocess_df(df: cudf.DataFrame, input_text_field: str = "text") -> cudf.DataFrame:
    ip = load_object_on_worker(
        "IndicProcessor", IndicProcessor, {"inference": True}
    )
    indices = df[input_text_field].index.to_arrow().to_pylist()
    sentences = df[input_text_field].to_arrow().to_pylist()
    sentences = ip.preprocess_batch(
        sentences, src_lang="eng_Latn", tgt_lang="hin_Deva"
    )
    df["indic_proc_text"] = cudf.Series(sentences, index=indices)
    return df


def has_alphabet_characters(text: str) -> bool:
    return any(c.isalpha() for c in text)


def atleast_letter(df: cudf.DataFrame, column_name: str) -> cudf.DataFrame:
    df = df.to_pandas()
    df["isalpha"] = df[column_name].apply(has_alphabet_characters)
    df = cudf.DataFrame(df)
    return df


def combine_text(df: cudf.DataFrame, input_text_field: str = "text") -> cudf.DataFrame:
    english_stop_flag = df[input_text_field].str.endswith(".")
    hindi_stop_flag = df["translation"].str.endswith("|")
    df["translation"][~english_stop_flag & hindi_stop_flag] = df[
        "translation"
    ].str.rstrip("|")
    df["translation"] = df["translation"].str.strip()
    return df


def grouping(df: cudf.DataFrame, input_text_field: str = "text") -> cudf.DataFrame:
    df = df.to_pandas()
    agg_funcs = {
        "translation": lambda s: "".join(s),
        input_text_field: lambda s: "".join(s),
    }
    other_columns = {
        col: "first"
        for col in df.columns
        if col not in agg_funcs and col != "doc_id"
    }

    agg_funcs.update(other_columns)
    df = df.groupby("doc_id").agg(agg_funcs).reset_index()
    df = cudf.DataFrame.from_pandas(df)
    return df


class IndicTranslation(DistributedDataClassifier):
    def __init__(
        self,
        pretrained_model_name_or_path: str = "ai4bharat/indictrans2-en-indic-1B",
        input_column: str = "text",
        batch_size: int = 128,
        autocast: bool = False,
    ):
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.input_column = input_column
        self.batch_size = batch_size
        self.autocast = autocast

        self.translation_config = TranslationConfig(
            pretrained_model_name_or_path=self.pretrained_model_name_or_path,
            max_length=256,
            num_beams=5,
            autocast=self.autocast,
        )
        self.model = ModelForSeq2SeqModel(self.translation_config)
        super().__init__(
            model=self.model,
            batch_size=self.batch_size,
            device_type="cuda",
            autocast=self.autocast,
            labels=None,
            filter_by=None,
            out_dim=None,
            pred_column=None,
            max_chars=None,
        )

    def _run_classifier(self, dataset: DocumentDataset) -> DocumentDataset:
        ddf = dataset.df
        # See process_input_text helper function defined above
        ddf = ddf.map_partitions(self.process_input_text, input_text_field=self.input_column, enforce_metadata=False)
        ddf[self.input_column] = ddf[self.input_column].astype("str")

        ddf["word_count"] = ddf[self.input_column].str.split().list.len()
        ddf["word_count"] = ddf["word_count"].astype("int64")
        ddf_true = ddf[(ddf["word_count"] <= self.translation_config.max_words_per_sen)]

        # Filter for at least one unicode letter in text
        # See atleast_letter helper function defined above
        has_letter = ddf_true.map_partitions(atleast_letter, column_name=self.input_column)
        ddf_trans = ddf_true[has_letter["isalpha"]]
        ddf = ddf_trans.drop(columns="word_count")

        ## ddf_false operations
        ddf_false = ddf_true[~has_letter["isalpha"]]
        ddf_false = ddf_false.drop(columns="word_count")
        ddf_false["translation"] = ddf_false[self.input_column]

        # Applying preprocess_df helper function for Indic preprocessing
        ddf[self.input_column] = ddf[self.input_column].astype("str")
        ddf_meta = ddf._meta.copy()
        ddf_meta["indic_proc_text"] = ""
        ddf = ddf.map_partitions(preprocess_df, input_text_field=self.input_column, meta=ddf_meta)

        columns = ddf.columns.tolist()
        pipe = op.Sequential(
            # This step tokenizes the input text found in the specified input_column
            op.Tokenizer(
                self.model, cols=[self.input_column], tokenizer_type="default"
            ),
            # The Predictor takes the tokenized input and passes it through the model to generate translations
            op.Predictor(
                self.model,
                sorted_data_loader=True,
                batch_size=self.batch_size,
                pred_output_col="translation",
            ),
            keep_cols=columns,
        )
        ddf = pipe(ddf)
        translated_meta = ddf._meta.copy()
        translated_meta["translation"] = "DUMMY_STRING"
        ddf = ddf.map_partitions(self.translate_tokens, meta=translated_meta)
        ddf = ddf.map_partitions(combine_text, input_text_field=self.input_column, meta=translated_meta)

        # Merging translated and non-translated samples
        ddf_true["false_translation"] = ddf_false["translation"]
        ddf_true["false_translation"] = ddf_true["false_translation"].fillna("")
        ddf_true["translation"] = ddf["translation"]
        ddf_true["translation"] = ddf_true["translation"].fillna("")
        ddf_true["translation"] = (
            ddf_true["translation"] + ddf_true["false_translation"]
        )

        # See grouping helper function defined above
        ddf = ddf_true.map_partitions(grouping, input_text_field=self.input_column)
        return DocumentDataset(ddf)

    def custom_tokenize(self, text: str):
        split_text = re.split(
            r"(\#{2,}|\_{2,}|\…{2,}|\+{2,}|\.{2,}|\-{3,}|\*{2,}|\~{2,}|\={2,}|\!{2,}|\n|\t|\‣|\⁃|\⁌|\⁍|\●|\○|\•|\·|\◘|\◦|\⦾|\⦿|\|)",
            text,
        )
        split_text = [s for s in split_text if len(s) > 0]
        tokenized_sentences = []
        len_flag = False
        for line in split_text:
            # Tokenize sentences using NLTK's sent_tokenize function
            if has_alphabet_characters(line) == True:
                sentences = sent_tokenize(line)
                i = 0
                j = 0
                curr_tokenized_snt = []
                non_translation_str = ""
                # Comparing the list of tokenized sentences (using NLTK) and actual the sentence,
                # preserving the spaces, newline and other special characters
                while i < len(line):
                    if j < len(sentences):
                        stripped_sent = sentences[j].strip()
                        if len(stripped_sent) == 0:
                            j += 1
                            continue
                        # If tokenized sentence matches, then moving to next sentence
                        if line[i] == stripped_sent[0]:
                            if non_translation_str != "":
                                curr_tokenized_snt.append(non_translation_str)
                            curr_tokenized_snt.append(stripped_sent)
                            i += len(stripped_sent)
                            j += 1
                            non_translation_str = ""
                        else:
                            non_translation_str += line[i]
                            i += 1
                    else:
                        non_translation_str += line[i]
                        i += 1
                if non_translation_str != "":
                    curr_tokenized_snt.append(non_translation_str)
                # Add the tokenized sentences to the list
                tokenized_sentences.extend(curr_tokenized_snt)
            else:
                tokenized_sentences.append(line)

        tokenized_sentence_len = []
        for sentence in tokenized_sentences:
            sent = sentence.split()
            # Removing the sentences with word length greater than threshold
            # Since the model may not be able translate it due to constraint on output token size
            if len(sent) <= self.translation_config.max_words_per_sen:
                tokenized_sentence_len.append(sentence)

        return tokenized_sentence_len

    def process_input_text(self, df: cudf.DataFrame, input_text_field: str = "text") -> cudf.DataFrame:
        df = df.to_pandas()
        df[input_text_field] = df[input_text_field].apply(self.custom_tokenize)
        df["doc_id"] = np.arange(1, len(df) + 1)
        df = df.explode(input_text_field, ignore_index=True)
        df = df.reset_index(drop=False)
        df = cudf.DataFrame.from_pandas(df)
        return df

    def translate_tokens(self, df: cudf.DataFrame) -> cudf.DataFrame:
        worker = get_worker()
        if hasattr(worker, "IndicProcessor"):
            ip = getattr(worker, "IndicProcessor")
        else:
            ip = load_object_on_worker(
                "IndicProcessor", IndicProcessor, {"inference": True}
            )
        tokenizer = self.model.load_tokenizer()
        indices = df["translation"].index.to_arrow().to_pylist()
        generated_tokens = df["translation"].to_arrow().to_pylist()
        with tokenizer.as_target_tokenizer():
            generated_tokens = tokenizer.batch_decode(
                generated_tokens,
                skip_special_tokens=True,
            )
        generated_tokens = ip.postprocess_batch(generated_tokens, lang="hin_Deva")
        df["translation"] = cudf.Series(data=generated_tokens, index=indices)
        return df


def main():
    device = "gpu"
    client = get_client(cluster_type=device)

    text = [
        "Quantum computing is set to revolutionize the field of cryptography.",
        "Investing in index funds is a popular strategy for long-term financial growth.",
        "Recent advancements in gene therapy offer new hope for treating genetic disorders.",
        "Online learning platforms have transformed the way students access educational resources.",
        "Traveling to Europe during the off-season can be a more budget-friendly option.",
        "Training regimens for athletes have become more sophisticated with the use of data analytics.",
        "Streaming services are changing the way people consume television and film content.",
        "Vegan recipes have gained popularity as more people adopt plant-based diets.",
        "Climate change research is critical for developing sustainable environmental policies.",
        "Telemedicine has become increasingly popular due to its convenience and accessibility.",
    ]
    df = cudf.DataFrame({"text": text})
    input_dataset = DocumentDataset(dask_cudf.from_cudf(df, npartitions=1))

    input_text_field = "text"
    batch_size = 128
    autocast = True

    translator_model = IndicTranslation(
        pretrained_model_name_or_path="ai4bharat/indictrans2-en-indic-1B",
        input_column=input_text_field,
        batch_size=batch_size,
        autocast=autocast,
    )

    result_dataset = translator_model(dataset=input_dataset)

    result_dataset.df.compute()


if __name__ == "__main__":
    main()
