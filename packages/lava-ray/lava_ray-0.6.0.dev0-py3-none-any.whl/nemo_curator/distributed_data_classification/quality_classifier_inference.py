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
import time
import warnings

os.environ["RAPIDS_NO_INITIALIZE"] = "1"
from nemo_curator import QualityClassifier
from nemo_curator.datasets import DocumentDataset
from nemo_curator.distributed_data_classification.arg_utils import create_arg_parser
from nemo_curator.utils.distributed_utils import get_client, read_data, write_to_disk
from nemo_curator.utils.file_utils import get_remaining_files

warnings.filterwarnings("ignore")


def add_quality_model_specific_args(parser):
    """
    This function adds a command line argument for the number of labels.

    Args:
        parser: An argparse ArgumentParser object.
    Returns:
        An argparse ArgumentParser with 1 additional argument.

    """
    parser.add_argument("--num-labels", type=int, default=3)
    return parser


def get_labels(num_labels):
    """
    This function returns a list of quality labels, depending on how many labels the user expects.

    Args:
        num_labels: An integer representing the number of possible classification labels.
    Returns:
        A list of label names.

    """
    if num_labels == 3:
        labels = ["High", "Medium", "Low"]
    elif num_labels == 2:
        labels = ["Medium_High", "Low"]
    return labels


def main():
    parser = create_arg_parser()
    parser = add_quality_model_specific_args(parser)
    args = parser.parse_args()
    labels = get_labels(args.num_labels)
    print(f"Arguments parsed = {args}", flush=True)
    max_chars = 6000

    client = get_client(args, cluster_type="gpu")
    print("Starting quality classifier inference", flush=True)
    global_st = time.time()
    files_per_run = len(client.scheduler_info()["workers"]) * 2

    if not os.path.exists(args.output_file_path):
        os.makedirs(args.output_file_path)

    input_files = get_remaining_files(
        args.input_file_path, args.output_file_path, args.input_file_type
    )
    print(f"Total input files {len(input_files)}", flush=True)

    if args.input_file_type == "pickle":
        add_filename = False
    else:
        add_filename = True

    classifier = QualityClassifier(
        model_file_name=args.model_file_name,
        max_chars=max_chars,
        labels=labels,
        batch_size=args.batch_size,
        autocast=args.autocast,
        out_dim=len(labels),
    )

    for file_batch_id, i in enumerate(range(0, len(input_files), files_per_run)):
        batch_st = time.time()
        current_batch_files = input_files[i : i + files_per_run]
        print(
            f"File Batch ID {file_batch_id}: total input files {len(current_batch_files)}",
            flush=True,
        )
        df = read_data(
            input_files=current_batch_files,
            file_type=args.input_file_type,
            add_filename=add_filename,
        )
        print(f"Total input Dask DataFrame partitions {df.npartitions}", flush=True)
        df = classifier(DocumentDataset(df)).df
        write_to_disk(
            df=df,
            output_file_dir=args.output_file_path,
            write_to_filename=add_filename,
        )
        batch_et = time.time()
        print(
            f"File Batch ID {file_batch_id}: completed in {batch_et-batch_st} seconds",
            flush=True,
        )

    global_et = time.time()
    print(
        f"Total time taken for quality classifier inference: {global_et-global_st} s",
        flush=True,
    )
    client.close()


def console_script():
    main()


if __name__ == "__main__":
    console_script()
