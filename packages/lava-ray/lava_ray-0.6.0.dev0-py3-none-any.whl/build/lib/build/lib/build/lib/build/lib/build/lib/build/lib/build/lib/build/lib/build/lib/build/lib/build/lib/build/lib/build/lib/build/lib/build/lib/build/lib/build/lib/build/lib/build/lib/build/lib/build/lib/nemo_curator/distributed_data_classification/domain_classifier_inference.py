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
from nemo_curator import DomainClassifier
from nemo_curator.datasets import DocumentDataset
from nemo_curator.distributed_data_classification.arg_utils import create_arg_parser
from nemo_curator.utils.distributed_utils import get_client, read_data, write_to_disk
from nemo_curator.utils.file_utils import get_remaining_files

warnings.filterwarnings("ignore")


def main():
    labels = [
        "Adult",
        "Arts_and_Entertainment",
        "Autos_and_Vehicles",
        "Beauty_and_Fitness",
        "Books_and_Literature",
        "Business_and_Industrial",
        "Computers_and_Electronics",
        "Finance",
        "Food_and_Drink",
        "Games",
        "Health",
        "Hobbies_and_Leisure",
        "Home_and_Garden",
        "Internet_and_Telecom",
        "Jobs_and_Education",
        "Law_and_Government",
        "News",
        "Online_Communities",
        "People_and_Society",
        "Pets_and_Animals",
        "Real_Estate",
        "Science",
        "Sensitive_Subjects",
        "Shopping",
        "Sports",
        "Travel_and_Transportation",
    ]

    args = create_arg_parser().parse_args()
    print(f"Arguments parsed = {args}", flush=True)
    max_chars = 2000

    client = get_client(args, cluster_type="gpu")
    print("Starting domain classifier inference", flush=True)
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

    domain_classifier = DomainClassifier(
        model_file_name=args.model_file_name,
        labels=labels,
        max_chars=max_chars,
        batch_size=args.batch_size,
        out_dim=len(labels),
        autocast=args.autocast,
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
        df = domain_classifier(DocumentDataset(df)).df
        print(f"Total input Dask DataFrame partitions {df.npartitions}", flush=True)

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
        f"Total time taken for domain classifier inference: {global_et-global_st} s",
        flush=True,
    )
    client.close()


def console_script():
    main()


if __name__ == "__main__":
    console_script()
