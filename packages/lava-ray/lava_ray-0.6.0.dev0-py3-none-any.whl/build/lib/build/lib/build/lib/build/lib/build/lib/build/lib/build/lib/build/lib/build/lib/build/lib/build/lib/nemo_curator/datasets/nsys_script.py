import torch
import time


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    a = torch.randn(100, 100, device=device)
    b = torch.randn(100, 100, device=device)

    start_time = time.time()
    c = torch.matmul(a, b)
    torch.cuda.synchronize()
    end_time = time.time()

    print(f"Matrix multiplication completed in {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()

def load_dataset(input_data_dir, file_type="parquet"):
    files = get_all_files_paths_under(input_data_dir)
    raw_data = read_data(files, file_type=file_type, backend="pandas", add_filename=True)
    dataset = DocumentDataset(raw_data)