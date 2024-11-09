import os
import argparse
import json

os.environ["DASK_DATAFRAME__QUERY_PLANNING"] = "False"
import dask_cudf

from nemo_curator import MinHash
from nemo_curator.datasets import DocumentDataset
from nemo_curator.utils.distributed_utils import get_client
from nemo_curator.utils.file_utils import get_all_files_paths_under
from nemo_curator.utils.script_utils import ArgumentHelper


def main(args):
    client = get_client(**ArgumentHelper.parse_client_args(args))

    print("Reading rpv2 data")
    files = get_all_files_paths_under(args.input_data_dir)[:3]
    df = dask_cudf.read_json(files, compression="gzip", lines=True)
    dataset = DocumentDataset(df)

    unique_count = df[args.minhash_id_field].nunique().compute()
    total_count = df[args.minhash_id_field].size.compute()
    print(unique_count)
    print(total_count)

    print("Computing minhashes")
    minhasher = MinHash(
        seed=args.seed,
        num_hashes=args.minhash_length,
        char_ngrams=args.char_ngram,
        use_64bit_hash=args.use_64bit_hash,
        logger=args.minhash_log_dir,
        id_field=args.minhash_id_field,
        text_field=args.minhash_text_field,
        cache_dir=args.output_data_dir,
    )
    res = minhasher(dataset).df
    print(res.head())

    client.close()


def attach_args(
    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    ),
):
    parser.add_argument(
        "--input-data-dir",
        type=str,
        default="/datasets/prospector-lm/rpv2/2022-33/EN/",
    )
    parser.add_argument(
        "--output-data-dir",
        type=str,
        default="/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/output/data",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--minhash-length",
        type=int,
        default=260,
    )
    parser.add_argument(
        "--char-ngram",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--use-64bit-hash",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--minhash-log-dir",
        type=str,
        default="/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/log",
    )
    parser.add_argument(
        "--minhash-id-field",
        type=str,
        default="digest",
    )
    parser.add_argument(
        "--minhash-text-field",
        type=str,
        default="raw_content",
    )

    return ArgumentHelper(parser).add_distributed_args()

if __name__ == "__main__":
    main(attach_args().parse_args())
