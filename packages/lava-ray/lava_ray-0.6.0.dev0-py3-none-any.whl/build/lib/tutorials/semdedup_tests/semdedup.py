import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from nemo_curator import get_client
from nemo_curator import SemDedup, SemDedupConfig
from nemo_curator.datasets import DocumentDataset
import yaml
import dask_cudf

"""
Have we tested that using single GPU, for a jsonl file how far are we in predicting 
memory use vs actual memory use. My hunch is error is from either of these:

- Incorrect Memory prediction
- Incorrect splitting
- Left over memory used in cache/memory leak

My suggestion is to somehow verify a and b, then lets look into c
"""

client = get_client(cluster_type="gpu")


print("Reading file")
df = dask_cudf.read_json("/datasets/semdedup/c4/en/modified/c4-train.00127-of-01024.json")#, lines=True)
# byte_range=(0, 805306372))
dataset = DocumentDataset(df)

print("Loading YAML")
with open("/home/nfs/syurick/NeMo-Curator/tutorials/semdedup_tests/semdedup_config.yaml", "r") as config_file:
    config_dict = yaml.safe_load(config_file)

print("Starting SemDeDup")
config = SemDedupConfig(**config_dict)
sem_dedup = SemDedup(config, logger="/home/nfs/syurick/NeMo-Curator/tutorials/semdedup_tests/log")
deduplicated_dataset_ids = sem_dedup(dataset)

print("Finished SemDeDup")

client.close()
