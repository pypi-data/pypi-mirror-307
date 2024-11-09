import os
import time

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import cudf
import numpy as np
import nvtx


def get_all_files_paths_under(root, recurse_subdirectories=True, followlinks=False):
    """
    This function returns a list of all the files under a specified directory.
    Args:
        root: The path to the directory to read.
        recurse_subdirecties: Whether to recurse into subdirectories.
                              Please note that this can be slow for large
                              number of files.
        followlinks: Whether to follow symbolic links.
    """
    if recurse_subdirectories:
        file_ls = [
            os.path.join(r, f)
            for r, subdirs, files in os.walk(root, followlinks=followlinks)
            for f in files
        ]
    else:
        file_ls = [entry.path for entry in os.scandir(root)]

    file_ls.sort()
    return file_ls


def generate_seeds(n_seeds: int = 260, seed: int = 0) -> np.ndarray:
    """
    Generate seeds for all minhash permutations based on the given seed.
    """
    gen = np.random.RandomState(seed)
    return gen.randint(0, 1e6, size=n_seeds)


def minhash32(
    ser: cudf.Series, seeds: np.ndarray, char_ngram: int
) -> cudf.Series:
    """
    Compute 32bit minhashes based on the MurmurHash3 algorithm
    """
    seeds = cudf.Series(seeds, dtype="uint32")
    return ser.str.minhash(seeds=seeds, width=char_ngram)


def main():
    input_data_dir = "/raid/prospector-lm/redpajama/data/"
    output_data_dir = "/home/nfs/syurick/NeMo-Curator/tutorials/rpv2_minhash_work/output/"
    seed = 10
    minhash_length = 260
    char_ngram = 24
    minhash_id_field = "adlr_id"
    minhash_text_field = "text"

    st = time.time()
    print("Reading data")
    nvtx.push_range("Reading data")
    files = get_all_files_paths_under(input_data_dir)[:char_ngram]
    df = cudf.read_json(files, lines=True)
    nvtx.pop_range()
    print(f"Time taken to read data: {time.time() - st}")

    st = time.time()
    print("Computing minhashes")
    nvtx.push_range("Computing minhashes")
    result = df[[minhash_id_field]]
    seeds = generate_seeds(n_seeds=minhash_length, seed=seed)
    result["_minhash_signature"] = minhash32(
        df[minhash_text_field], seeds=seeds, char_ngram=char_ngram
    )
    write_path = os.path.join(output_data_dir, "_minhashes.parquet")
    nvtx.pop_range()
    print(f"Time taken to compute minhashes: {time.time() - st}")

    st = time.time()
    print("Writing data")
    nvtx.push_range("Writing data")
    result.to_parquet(write_path)
    nvtx.pop_range()
    print(f"Time taken to write data: {time.time() - st}")


if __name__ == "__main__":
    main()
