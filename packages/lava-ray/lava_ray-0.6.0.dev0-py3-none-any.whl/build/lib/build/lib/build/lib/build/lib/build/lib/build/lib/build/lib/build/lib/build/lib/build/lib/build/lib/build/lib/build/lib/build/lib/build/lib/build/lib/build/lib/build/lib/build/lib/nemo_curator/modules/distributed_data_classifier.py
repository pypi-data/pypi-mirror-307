# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

os.environ["RAPIDS_NO_INITIALIZE"] = "1"
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import torch
import torch.nn as nn
from crossfit import op
from crossfit.backend.torch.hf.model import HFModel
from huggingface_hub import PyTorchModelHubMixin
from transformers import AutoConfig, AutoModel, AutoTokenizer
from transformers.models.deberta_v2 import DebertaV2TokenizerFast

from nemo_curator.datasets import DocumentDataset

from torch.utils.data import Dataset
from nemo_curator.utils.distributed_utils import load_object_on_worker

DOMAIN_IDENTIFIER = "nvidia/domain-classifier"


@dataclass
class DomainModelConfig:
    model = "microsoft/deberta-v3-base"
    fc_dropout = 0.2
    max_len = 512


@dataclass
class QualityModelConfig:
    model = "microsoft/deberta-v3-base"
    fc_dropout = 0.2
    max_len = 512


# TODO: Remove this class after Quality Model is uploaded to HuggingFace
class NCCustomModel(nn.Module):
    def __init__(
        self,
        config: dataclass,
        out_dim: int,
        config_path: str = None,
        pretrained: bool = False,
        autocast: bool = False,
    ):
        super().__init__()
        self.config = config
        if config_path is None:
            self.config = AutoConfig.from_pretrained(
                config.model, output_hidden_states=True
            )
        else:
            self.config = torch.load(config_path)

        if pretrained:
            self.model = AutoModel.from_pretrained(config.model, config=self.config)
        else:
            self.model = AutoModel(self.config)

        self.fc_dropout = nn.Dropout(config.fc_dropout)
        self.fc = nn.Linear(self.config.hidden_size, out_dim)
        self._init_weights(self.fc)
        self.autocast = autocast

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)

    def feature(self, input_ids, attention_mask):
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_states = outputs[0]
        return last_hidden_states

    def _forward(self, batch):
        feature = self.feature(batch["input_ids"], batch["attention_mask"])
        output = self.fc(self.fc_dropout(feature))
        output = output.to(torch.float32)
        return torch.softmax(output[:, 0, :], dim=1)

    def forward(self, batch):
        if self.autocast:
            with torch.autocast(device_type="cuda"):
                return self._forward(batch)
        else:
            return self._forward(batch)


class HFCustomModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config: dataclass):
        super(HFCustomModel, self).__init__()
        self.model = AutoModel.from_pretrained(config["base_model"])
        self.dropout = nn.Dropout(config["fc_dropout"])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config["id2label"]))

    def _forward(self, batch):
        features = self.model(
            batch["input_ids"], batch["attention_mask"]
        ).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)

    def forward(self, batch):
        if self.autocast:
            with torch.autocast(device_type="cuda"):
                return self._forward(batch)
        else:
            return self._forward(batch)

    def set_autocast(self, autocast):
        self.autocast = autocast


class DistributedDataClassifier(ABC):
    """Abstract class for running multi-node multi-GPU data classification"""

    def __init__(
        self,
        model,
        labels,
        filter_by,
        batch_size,
        out_dim,
        pred_column,
        max_chars,
        device_type,
        autocast,
    ):
        self.model = model
        self.labels = labels
        self.filter_by = filter_by
        self.batch_size = batch_size
        self.out_dim = out_dim
        self.pred_column = pred_column
        self.max_chars = max_chars
        self.device_type = device_type
        self.autocast = autocast

    def __call__(self, dataset: DocumentDataset):
        result_doc_dataset = self._run_classifier(dataset)
        if self.filter_by is not None:
            return self._filter_documents(result_doc_dataset)

        return result_doc_dataset

    @abstractmethod
    def _run_classifier(self):
        pass

    def _filter_documents(
        self,
        dataset: DocumentDataset,
    ):
        df = dataset.df

        filter_by = self.filter_by
        if type(filter_by) == str:
            filtered_df = df[df[self.pred_column].astype(str) == filter_by]
            return DocumentDataset(filtered_df)
        elif type(filter_by) == list:
            filtered_df = df[df[self.pred_column].isin(filter_by)]
            return DocumentDataset(filtered_df)

        raise TypeError("filter_by must be a string or list type")

    def get_labels(self) -> List[str]:
        return self.labels

    def _cfg_per_partition(self):
        return load_object_on_worker(
            "cfg_with_tokenizer",
            self._load_cfg_with_tokenizer,
            {},
        )


def _run_classifier_helper(
    df: "dask_cudf.DataFrame",
    model: "HFModel",
    labels: list[str],
    max_chars: int,
    batch_size: int,
    label_col: str,
    prob_col: str = None,
) -> "dask_cudf.DataFrame":

    keep_prob = prob_col is not None
    prob_internal_col = "_prob"
    # TODO: Make crossfit handle this cleanly
    pred_internal_col = "labels"
    df["sliced_text"] = df["text"].str.slice(0, max_chars)
    columns_to_keep_list = df.columns.to_list()
    columns_to_keep_list.remove("sliced_text")

    classifier_pipe = op.Sequential(
        op.Tokenizer(model, cols=["sliced_text"], tokenizer_type="sentencepiece"),
        op.Predictor(
            model,
            sorted_data_loader=True,
            batch_size=batch_size,
            pred_output_col=prob_internal_col,
        ),
        repartition=df.npartitions,
        keep_cols=columns_to_keep_list,
    )
    df = classifier_pipe(df)

    # TODO: Make crossfit handle this cleanly
    # to prevent the labeler from dropping the prob_internal_col
    # and combine it into a single step
    labeling_pipe = op.Sequential(
        op.Labeler(labels, cols=[prob_internal_col]),
        keep_cols=columns_to_keep_list + [prob_internal_col],
    )
    df = labeling_pipe(df)

    if keep_prob:
        df = df.rename(
            columns={prob_internal_col: prob_col, pred_internal_col: label_col},
        )
    else:
        df = df.rename(columns={pred_internal_col: label_col})
        df = df.drop(columns=[prob_internal_col])

    return df


class DomainModel(HFModel):
    def __init__(self, config: dataclass, autocast: bool = False):
        self.config = config
        self.autocast = autocast
        super().__init__(self.config.model)

    def load_model(self, device="cuda"):
        model = HFCustomModel.from_pretrained(DOMAIN_IDENTIFIER)
        model.set_autocast(self.autocast)
        model = model.to(device)
        return model.eval()

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(DOMAIN_IDENTIFIER)

    def load_config(self):
        return AutoConfig.from_pretrained(DOMAIN_IDENTIFIER)


class QualityModel(HFModel):
    def __init__(self, config, out_dim=None, model_path=None, autocast=False):
        self.config = config
        self.out_dim = out_dim
        self.model_path = model_path
        self.autocast = autocast
        super().__init__(self.config.model)

    def load_model(self, device="cuda"):
        model = NCCustomModel(
            self.config,
            out_dim=self.out_dim,
            config_path=None,
            pretrained=True,
            autocast=self.autocast,
        )
        model = model.to(device)

        if os.path.exists(self.model_path):
            sd = torch.load(self.model_path, map_location="cpu")
            if "model_state_dict" in sd:
                sd = sd["model_state_dict"]
            sd = {k[7:] if k.startswith("module.") else k: sd[k] for k in sd.keys()}
            model.load_state_dict(sd, strict=True)
        else:
            raise ValueError(f"Model path {self.model_path} does not exist")

        return model.eval()

    def load_tokenizer(self):
        return DebertaV2TokenizerFast.from_pretrained(self.config.model)

    def load_config(self):
        return AutoConfig.from_pretrained(self.path_or_name)


class DomainClassifier(DistributedDataClassifier):
    def __init__(
        self,
        filter_by=None,
        batch_size=256,
        pred_column="domain_pred",
        prob_column=None,
        max_chars=2000,
        device_type="cuda",
        autocast=True,
    ):
        config = AutoConfig.from_pretrained(DOMAIN_IDENTIFIER)

        self.prob_column = prob_column
        self.labels = list(config.label2id.keys())
        self.out_dim = len(self.labels)

        model = DomainModel(config=DomainModelConfig, autocast=autocast)

        super().__init__(
            model=model,
            labels=self.labels,
            filter_by=filter_by,
            batch_size=batch_size,
            out_dim=self.out_dim,
            pred_column=pred_column,
            max_chars=max_chars,
            device_type=device_type,
            autocast=autocast,
        )

    def _run_classifier(self, dataset: DocumentDataset):
        print("Starting domain classifier inference", flush=True)
        df = dataset.df
        df = _run_classifier_helper(
            df=df,
            model=self.model,
            labels=self.labels,
            max_chars=self.max_chars,
            batch_size=self.batch_size,
            label_col=self.pred_column,
            prob_col=self.prob_column,
        )
        return DocumentDataset(df)


class TestDataset(Dataset):
    def __init__(self, cfg, df, max_chars):
        self.cfg = cfg
        text = df["text"].str.slice(0, max_chars).to_arrow().to_pylist()
        with torch.no_grad():
            self.tokens = cfg.tokenizer.batch_encode_plus(
                text,
                return_tensors="pt",
                add_special_tokens=True,
                max_length=cfg.max_len,
                pad_to_max_length=True,
                truncation=True,
                return_token_type_ids=False,
            )
        self.max_chars = max_chars
        self.dataset_len = len(text)

    def __len__(self):
        return self.dataset_len

    def __getitem__(self, item):
        return {k: v[item] for k, v in self.tokens.items()}


def process_batch(
    load_model_function, load_model_kwargs, run_inference_function, run_inference_kwargs
):
    """
    This function loads a model on a Dask worker and then runs inference on a batch of data.

    Args:
        load_model_function: A user-provided function for loading a classifier.
        load_model_kwargs: A dictionary of arguments necessary for `load_model_function`.
        run_inference_function: A user-provided function for running inference, which has a "model" argument.
        run_inference_kwargs: A dictionary of arguments necessary for `run_inference_function`.
    Returns:
        Whatever `run_inference_function` returns, such as a list or tensor of predictions.

    """
    model = load_object_on_worker("model", load_model_function, load_model_kwargs)
    return run_inference_function(**run_inference_kwargs, model=model)


def process_all_batches(
    loader_valid,
    load_model_function,
    load_model_kwargs,
    run_inference_function,
    run_inference_kwargs,
):
    """
    This function iterates over batches of data, loading a model and running inference per batch.

    Args:
        loader_valid: An iterable data object, such as a PyTorch DataLoader.
        load_model_function: A user-provided function for loading a classifier.
        load_model_kwargs: A dictionary of arguments necessary for `load_model_function`.
        run_inference_function: A user-provided function for running inference, which has "model" and "batch" arguments.
        run_inference_kwargs: A dictionary of arguments necessary for `run_inference_function`.
    Returns:
        A tensor of predictions for all batches of the data.

    """
    import torch

    return torch.cat(
        [
            process_batch(
                load_model_function,
                load_model_kwargs,
                run_inference_function,
                dict(run_inference_kwargs, batch=batch),
            )
            for batch in loader_valid
        ]
    )


class CFG:
    model = "microsoft/deberta-v3-base"
    fc_dropout = 0.2

    def __init__(self, max_len=512):
        self.max_len = max_len


def collate(inputs):
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    mask_len = int(inputs["attention_mask"].sum(axis=1).max())
    for k, v in inputs.items():
        # CPMP: no need to truncate labels
        if k != "labels":
            inputs[k] = inputs[k][:, :mask_len]
    return inputs


class QualityClassifier(DistributedDataClassifier):
    def __init__(
        self,
        model_path,
        num_labels=3,
        filter_by=None,
        batch_size=256,
        pred_column="quality_pred",
        prob_column="quality_prob",
        max_chars=6000,
        device_type="cuda",
        autocast=True,
    ):
        self.max_len = 1024
        self.num_workers = 0
        self.model_path = model_path
        self.binary_classification = False
        if num_labels == 3:
            self.labels = ["High", "Medium", "Low"]
            self.out_dim = num_labels  # Multiclass classification
        elif num_labels == 2:
            self.labels = ["Medium_High", "Low"]
            self.out_dim = 1  # Binary classification
        else:
            raise ValueError("num_labels must be 2 or 3")

        self.prob_column = prob_column

        model = QualityModel(
            config=QualityModelConfig,
            out_dim=self.out_dim,
            model_path=model_path,
            autocast=autocast,
        )

        super().__init__(
            model=model,
            labels=self.labels,
            filter_by=filter_by,
            batch_size=batch_size,
            out_dim=self.out_dim,
            pred_column=pred_column,
            max_chars=max_chars,
            device_type=device_type,
            autocast=autocast,
        )

    """def _run_classifier(self, dataset: DocumentDataset):
        print("Starting Quality classifier inference", flush=True)
        df = dataset.df
        df = _run_classifier_helper(
            df=df,
            model=self.model,
            labels=self.labels,
            max_chars=self.max_chars,
            batch_size=self.batch_size,
            label_col=self.pred_column,
            prob_col=self.prob_column,
        )
        return DocumentDataset(df)
    """

    def _load_cfg_with_tokenizer(self):
        cfg = CFG(max_len=self.max_len)
        tokenizer = DebertaV2TokenizerFast.from_pretrained(cfg.model)
        cfg.tokenizer = tokenizer
        return cfg

    def _run_classifier(self, dataset: DocumentDataset):
        print("Starting quality classifier inference", flush=True)

        df = dataset.df

        meta_df = df._meta.copy()
        meta_df[self.pred_column] = ["low"] * len(meta_df)
        meta_df[self.prob_column] = [[0, 0, 1]] * len(meta_df)

        df = df.map_partitions(
            self._inference_per_partition,
            meta=meta_df,
            enforce_metadata=False,
        )

        return DocumentDataset(df)

    def _inference_per_partition(self, df):
        cfg = self._cfg_per_partition()

        dataset_valid = TestDataset(cfg, df, self.max_chars)
        loader_valid = torch.utils.data.DataLoader(
            dataset_valid,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
        )
        device = torch.device(self.device_type)
        if len(self.labels) == 1:
            raise ValueError("Labels must be more than 1")

        load_model_kwargs = {
            "cfg": cfg,
            "device": device,
        }

        probs = process_all_batches(
            loader_valid,
            self._load_model,
            load_model_kwargs,
            self._run_inference,
            {},
        )

        if self.binary_classification:
            preds = (probs > 0.5).to(torch.int64).squeeze()
        else:
            preds = torch.argmax(probs, dim=1)

        df[self.pred_column] = [
            self.labels[i] for i in preds.to("cpu").numpy().tolist()
        ]
        df[self.prob_column] = probs.to("cpu").numpy().tolist()

        return df

    def _load_model(self, cfg, device):
        model = NCCustomModel(
            cfg, out_dim=self.out_dim, config_path=None, pretrained=True
        )
        model = model.to(device)
        sd = torch.load(self.model_path, map_location="cpu")
        if "model_state_dict" in sd:
            sd = sd["model_state_dict"]
        sd = {k[7:] if k.startswith("module.") else k: sd[k] for k in sd.keys()}
        model.load_state_dict(sd, strict=True)
        model.eval()
        return model

    def _run_inference(self, batch, model):
        with torch.no_grad():
            batch = collate(batch)
            if self.autocast:
                with torch.autocast(device_type=self.device_type):
                    # TODO
                    try:
                        out = model(batch)[:, 0, :]
                    except IndexError:
                        out = model(batch)
            else:
                out = model(batch)[:, 0, :]
            if self.binary_classification:
                probs = torch.sigmoid(out)
            else:
                probs = torch.softmax(out, dim=1)
        return probs
