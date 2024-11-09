import os

# from dask.dataframe.utils import assert_eq
from distributed import Client

from nemo_curator import SemDedup, SemDedupConfig
from nemo_curator.datasets import DocumentDataset

import cudf
import dask_cudf
from dask_cuda import LocalCUDACluster


def main():
    df = cudf.DataFrame(
        {
            "id": [1, 2, 3, 4, 100, 200, 300],
            "text": [
                "The quick brown fox jumps over the lazy dog",
                "The quick brown foxes jumps over the lazy dog",
                "The quick brown wolf jumps over the lazy dog",
                "The quick black cat jumps over the lazy dog",
                "A test string",
                "Another test string",
                "A different object",
            ],
        }
    )
    df = dask_cudf.from_cudf(df, 2)
    dedup_data = DocumentDataset(df)

    cluster = LocalCUDACluster(n_workers=1)
    client = Client(cluster)

    print("client", client)
    cache_dir = os.path.join("/home/nfs/syurick/NeMo-Curator/tests/tmpdir", "test_sem_dedup_cache")
    config = SemDedupConfig(
        cache_dir=cache_dir,
        id_col_name="id",
        id_col_type="int",
        input_column="text",
        seed=42,
        n_clusters=3,
        eps_thresholds=[0.10],
        eps_to_extract=0.10,
    )
    sem_duplicates = SemDedup(config=config)
    result = sem_duplicates(dedup_data)
    result_df = result.df.compute()
    duplicate_docs = [2, 3, 4, 200, 300]
    expected_df = cudf.Series(duplicate_docs, name="id")

    # assert_eq(result_df["id"].sort_values(), expected_df, check_index=False)
    print(result_df["id"].sort_values())
    print("*")
    print(expected_df)

if __name__ == "__main__":
    main()
