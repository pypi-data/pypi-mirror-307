from nemo_curator.image.embedders import TimmImageEmbedder
from nemo_curator.image.classifiers import AestheticClassifier, NsfwClassifier
from nemo_curator.datasets import ImageTextPairDataset
from nemo_curator import get_client, Sequential


def aesthetic_example():
    client = get_client(cluster_type="gpu")

    webdataset_path = "/datasets/mscoco/mscoco"
    output_path = "/datasets/mscoco/syurick_aesthetic_output"
    id_col = "key"

    dataset = ImageTextPairDataset.from_webdataset(webdataset_path, id_col)
    dataset.metadata = dataset.metadata[dataset.metadata["error_message"].isna()]

    aesthetic_pipeline = Sequential(
        [
            TimmImageEmbedder(
                "vit_large_patch14_clip_quickgelu_224.openai",  # 768 embedding dim
                pretrained=True,
                batch_size=1024,
                num_threads_per_worker=16,
            ),
            AestheticClassifier(),
        ]
    )
    new_dataset = aesthetic_pipeline(dataset)

    new_dataset.save_metadata(output_path)


def nsfw_example():
    client = get_client(cluster_type="gpu")

    webdataset_path = "/datasets/mscoco/mscoco"
    output_path = "/datasets/mscoco/syurick_nsfw_output"
    id_col = "key"

    dataset = ImageTextPairDataset.from_webdataset(webdataset_path, id_col)
    dataset.metadata = dataset.metadata[dataset.metadata["error_message"].isna()]

    nsfw_pipeline = Sequential(
        [
            TimmImageEmbedder(
                "vit_huge_patch14_clip_224.laion2b",  # 768 embedding dim
                pretrained=True,
                batch_size=1024,
                num_threads_per_worker=16,
            ),
            NsfwClassifier(),
        ]
    )
    new_dataset = nsfw_pipeline(dataset)

    new_dataset.save_metadata(output_path)


if __name__ == "__main__":
  print("Running AestheticClassifier")
  aesthetic_example()
