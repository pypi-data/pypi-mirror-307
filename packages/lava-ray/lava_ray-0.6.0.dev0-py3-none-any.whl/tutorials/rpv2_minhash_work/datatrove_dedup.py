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
from datatrove.utils.text import TextNormConfig

# you can also change ngrams or the number of buckets and their size here
textnormconfig = TextNormConfig(lowercase=False, norm_whitespace=False, remove_punctuation=False, norm_unicode_diacritics=False, norm_numbers=False, norm_weekdays=False, norm_monthnames=False)
minhash_config = MinhashConfig(use_64bit_hashes=False, num_buckets=20, hashes_per_bucket=13, seed=42, norm_config=textnormconfig)  # better precision -> fewer false positives (collisions)

MINHASH_BASE_PATH = "/raid/adattagupta/nemo-data-curator/minhash_experiment/books3/v2/datatrove_out"

LOGS_FOLDER = "/raid/adattagupta/nemo-data-curator/minhash_experiment/books3/v2/datatrove_log"
LOCAL_LOGS_FOLDER = "/raid/adattagupta/nemo-data-curator/minhash_experiment/books3/v2/datatrove_log"

TOTAL_TASKS = 998

# this is the original data that we want to deduplicate
INPUT_READER = JsonlReader("/raid/prospector-lm/Books3_shuf/resharded/", id_key="adlr_id", text_key="text")

# stage 1 computes minhash signatures for each task (each task gets a set of files)
stage1 = LocalPipelineExecutor(
    pipeline=[
        INPUT_READER,
        MinhashDedupSignature(output_folder=f"{MINHASH_BASE_PATH}/signatures", config=minhash_config),
    ],
    logging_dir=f"{LOGS_FOLDER}/signatures",
    tasks=TOTAL_TASKS,
    workers=96,
)

# stage 2 finds matches between signatures in each bucket
stage2 = LocalPipelineExecutor(
    pipeline=[
        MinhashDedupBuckets(
            input_folder=f"{MINHASH_BASE_PATH}/signatures",
            output_folder=f"{MINHASH_BASE_PATH}/buckets",
            config=minhash_config,
        ),
    ],
    tasks=minhash_config.num_buckets,
    logging_dir=f"{LOGS_FOLDER}/buckets",
    depends=stage1,
    workers=96,
)

stage3 = LocalPipelineExecutor(
    pipeline=[
        MinhashDedupCluster(
            input_folder=f"{MINHASH_BASE_PATH}/buckets",
            output_folder=f"{MINHASH_BASE_PATH}/remove_ids",
            save_cluster_id=True,
            config=minhash_config,
        ),
    ],
    tasks=1,
    depends=stage2,
    logging_dir=f"{LOGS_FOLDER}/clusters",
    workers=96,
)
run_stage4 = True
if run_stage4:
    # stage 4 reads the original input data and removes all but 1 sample per duplicate cluster
    # the data must match exactly stage 1, so number of tasks and the input source must be the same
    stage4 = LocalPipelineExecutor(
        pipeline=[
            INPUT_READER,
            #TokensCounter(),  # nice way to see how many tokens we had before and after deduplication
            MinhashDedupFilter(
                input_folder=f"{MINHASH_BASE_PATH}/remove_ids",
                exclusion_writer=JsonlWriter(f"{MINHASH_BASE_PATH}/removed"),
                load_cluster_ids=True,
            ),
            JsonlWriter(output_folder=f"{MINHASH_BASE_PATH}/deduplicated_output", compression=None),
        ],
        tasks=TOTAL_TASKS,
        logging_dir=f"{LOGS_FOLDER}/filter",
        depends=stage3,
        workers=96,
    )
if __name__ == "__main__":
    #stage1.run()
    #stage2.run()
    #stage3.run()
    #breakpoint()
    stage4.run()
