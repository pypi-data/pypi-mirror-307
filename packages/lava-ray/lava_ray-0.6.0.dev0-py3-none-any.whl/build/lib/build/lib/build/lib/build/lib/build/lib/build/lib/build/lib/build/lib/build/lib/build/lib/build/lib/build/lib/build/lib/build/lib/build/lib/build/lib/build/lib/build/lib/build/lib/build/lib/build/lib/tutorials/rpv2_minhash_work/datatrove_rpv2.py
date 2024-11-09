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


input_path = "/datasets/syurick/rpv2/"
st = str(time.time())
RESULTS_PATH = f"/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/datatrove_output_{st}/"
LOGS_FOLDER = f"/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/log_{st}"

seed = 10
char_ngram = 24
id_field = "digest"
text_field = "raw_content"
workers = char_ngram

hash_config = HashConfig(precision=32)
minhash_config = MinhashConfig(
    n_grams=char_ngram,
    # minhash_length = 260 = 20 * 13
    num_buckets=20,
    hashes_per_bucket=13,
    seed=seed,
    hash_config=hash_config,
)

ENGLISH_PATTERN = "*/EN/*.json.gz"
YEAR_2022_PATTERN = "2022-*/*/*.json.gz"

TOTAL_TASKS = char_ngram
INPUT_READER = JsonlReader(
    input_path,
    # limit=char_ngram,  # For debugging
    text_key=text_field,
    id_key=id_field,
    glob_pattern=ENGLISH_PATTERN, # Filter to only English
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

    stage2 = LocalPipelineExecutor(
        pipeline=[
            MinhashDedupBuckets(
                input_folder=f"{RESULTS_PATH}/signatures",
                output_folder=f"{RESULTS_PATH}/buckets",
                config=minhash_config,
            ),
        ],
        tasks=minhash_config.num_buckets,
        logging_dir=f"{LOGS_FOLDER}/2-buckets",
        depends=stage1,
    )

    stage3 = LocalPipelineExecutor(
        pipeline=[
            MinhashDedupCluster(
                input_folder=f"{RESULTS_PATH}/buckets",
                output_folder=f"{RESULTS_PATH}/remove_ids",
                config=minhash_config,
            ),
        ],
        tasks=1,
        logging_dir=f"{LOGS_FOLDER}/3-clusters",
        depends=stage2,
    )

    stage4 = LocalPipelineExecutor(
        pipeline=[
            INPUT_READER,
            TokensCounter(),
            MinhashDedupFilter(
                input_folder=f"{RESULTS_PATH}/remove_ids",
                exclusion_writer=JsonlWriter(f"{RESULTS_PATH}/removed_output", compression=None),
            ),
            JsonlWriter(output_folder=f"{RESULTS_PATH}/retained_output", compression=None),
        ],
        tasks=TOTAL_TASKS,
        logging_dir=f"{LOGS_FOLDER}/4-filter",
        depends=stage3,
    )

    stage4.run()


if __name__ == "__main__":
    run_local()
