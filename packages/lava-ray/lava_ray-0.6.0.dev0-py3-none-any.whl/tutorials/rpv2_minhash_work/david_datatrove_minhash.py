import time

from datatrove.executor.local import LocalPipelineExecutor
from datatrove.pipeline.dedup import MinhashDedupSignature
from datatrove.pipeline.dedup.minhash import (
    MinhashConfig,
    MinhashDedupBuckets,
    MinhashDedupCluster,
    MinhashDedupFilter,
)
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.tokens import TokensCounter
from datatrove.pipeline.writers.jsonl import JsonlWriter
from datatrove.utils.hashing import HashConfig


# Has 24 files
input_path = "/raid/prospector-lm/syurick/redpajama/data_sample"
st = str(time.time())
RESULTS_PATH = f"/raid/prospector-lm/syurick/redpajama/datatrove_output_{st}/"
LOGS_FOLDER = f"/raid/prospector-lm/syurick/redpajama/log_{st}"

# Sample values to set here
seed = 10
char_ngram = 5
id_field = "adlr_id"
text_field = "text"

# TODO: Test with and without custom textnorm_config
textnorm_config = TextNormConfig(
    lowercase=False,
    norm_whitespace=False,
    remove_punctuation=False,
    norm_unicode_diacritics=False,
    norm_numbers=False,
    norm_weekdays=False,
    norm_monthnames=False,
)

# Since we are passing in 24 files
TOTAL_TASKS = 24

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

ENGLISH_PATTERN = "*/EN/*.json.gz"
YEAR_2022_PATTERN = "2022-*/*/*.json.gz"
INPUT_READER = JsonlReader(
    input_path,
    # limit=char_ngram,  # For debugging
    text_key=text_field,
    id_key=id_field,
    # glob_pattern=ENGLISH_PATTERN, # Filter to only English
    # glob_pattern=YEAR_2022_PATTERN,  # Filter to only 2022
)

def run_local():
    stage1 = LocalPipelineExecutor(
        pipeline=[
            INPUT_READER,
            MinhashDedupSignature(output_folder=f"{RESULTS_PATH}/signatures", config=minhash_config),
        ],
        tasks=TOTAL_TASKS,
        logging_dir=f"{LOGS_FOLDER}/1-signatures",
    )

    stage1.run()


if __name__ == "__main__":
    run_local()
