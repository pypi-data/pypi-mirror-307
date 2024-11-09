from datatrove.executor.local import LocalPipelineExecutor
from datatrove.pipeline.dedup import MinhashDedupSignature
from datatrove.pipeline.dedup.minhash import MinhashConfig
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers.jsonl import JsonlWriter
from datatrove.utils.text import TextNormConfig
from datatrove.utils.hashing import HashConfig
import time

input_data_dir = "/raid/prospector-lm/redpajama/data/"
st = str(time.time())
output_data_dir = f"/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/datatrove_output_{st}/"
log_dir = f"/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/log_{st}"

seed = 10
char_ngram = 24
minhash_id_field = "adlr_id"
minhash_text_field = "text"

textnorm_config = TextNormConfig(
    lowercase=False,
    norm_whitespace=False,
    remove_punctuation=False,
    norm_unicode_diacritics=False,
    norm_numbers=False,
    norm_weekdays=False,
    norm_monthnames=False,
)
hash_config = HashConfig(precision=32)
minhash_config = MinhashConfig(
    n_grams=char_ngram,
    # minhash_length = 260 = 20 * 13
    num_buckets=20,
    hashes_per_bucket=13,
    seed=seed,
    norm_config=textnorm_config,
    hash_config=hash_config,
)

jsonl_reader = JsonlReader(
    input_data_dir, limit=char_ngram, text_key=minhash_text_field, id_key=minhash_id_field
)

stage1 = LocalPipelineExecutor(
    pipeline=[
        jsonl_reader,
        MinhashDedupSignature(output_folder=f"{output_data_dir}/signatures", config=minhash_config),
    ],
    logging_dir=f"{log_dir}/signatures",
    tasks=char_ngram,
    workers=char_ngram,
)


if __name__ == "__main__":
    stage1.run()
