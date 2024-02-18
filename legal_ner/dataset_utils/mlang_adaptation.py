import json
from typing import Dict, List

import numpy as np


def map_datasets(datasets_to_map: List[str], mapped_datasets: List[str], labels_mapping: Dict[str, str]) -> None:
    """Map all the annotation labels of a given dataset according to a dictionary

    Args:
        datasets_to_map (List[str]): The input file names of the datasets to map
        mapped_datasets (List[str]): The output file names of the mapped datasets
        labels_mapping (Dict[str, str]): A dictionary containing the mapping for each label
    """

    for to_map, mapped in zip(datasets_to_map, mapped_datasets):
        with open(to_map) as f:
            dataset = json.load(f)
            for row in dataset:
                for annotation in row["annotations"][0]["result"]:
                    annotation["value"]["labels"] = [labels_mapping[label]
                                                     for label in annotation["value"]["labels"]]

            with open(mapped, "w") as fp:
                json.dump(dataset, fp)


def reduce_datasets(datasets_to_reduce: List[str], reduced_datasets: List[str]) -> None:
    """Reduce all the datasets to the size of the smallest given one by choosing random rows

    Args:
        datasets_to_reduce (List[str]): The input file names of the datasets to reduce
        reduced_datasets (List[str]): The output file names of the reduced datasets
    """

    files = []

    try:
        datasets = []

        for dataset_to_reduce in datasets_to_reduce:
            file = open(dataset_to_reduce, "r")
            files.append(file)
            datasets.append(json.load(file))

        min_size = min([len(dataset) for dataset in datasets])

        for dataset, reduced in zip(datasets, reduced_datasets):

            choices = np.random.choice(
                len(dataset), min_size, replace=False)

            new_dataset = [dataset[i] for i in choices]

            with open(reduced, "w") as fp:
                json.dump(new_dataset, fp)

    finally:
        for file in files:
            file.close()


def merge_datasets(datasets_to_merge: List[str], merged_dataset: str) -> None:
    """Merge all the given datasets into a big unique one

    Args:
        datasets_to_merge (List[str]): The input file names of the datasets to merge
        merged_dataset (str): The output file name of the merged dataset
    """

    merged = []

    for dataset_name in datasets_to_merge:
        with open(dataset_name) as f:
            dataset = json.load(f)

            merged = merged + dataset

    with open(merged_dataset, "w") as fp:
        json.dump(merged, fp)


def main() -> None:

    # ################################
    # Map datasets
    # ################################

    de_datasets_to_map = ["de_train.json", "de_validation.json"]
    de_mapped_datasets = ["de_train_mapped.json", "de_val_mapped.json"]
    de_labels_mapping = {"LIT": "LEGAL",
                         "LOC": "LOC",
                         "NRM": "LEGAL",
                         "ORG": "ORG",
                         "PER": "PER",
                         "REG": "LEGAL",
                         "RS": "LEGAL"}

    en_datasets_to_map = ["en_train.json", "en_val.json"]
    en_mapped_datasets = ["en_train_mapped.json", "en_val_mapped.json"]
    en_labels_mapping = {"COURT": "LEGAL",
                         "PETITIONER": "PER",
                         "RESPONDENT": "PER",
                         "JUDGE": "PER",
                         "DATE": "TIME",  # TODO Think if keep it
                         "ORG": "ORG",
                         "GPE": "LOC",
                         "STATUTE": "LEGAL",
                         "PROVISION": "LEGAL",
                         "PRECEDENT": "LEGAL",
                         "CASE_NUMBER": "LEGAL",
                         "WITNESS": "PER",
                         "OTHER_PERSON": "PER",
                         "LAWYER": "PER"}

    es_datasets_to_map = ["es_train.json", "es_val.json"]
    es_mapped_datasets = ["es_train_mapped.json", "es_val_mapped.json"]
    es_labels_mapping = {"legal": "LEGAL",
                         "per": "PER",
                         "org": "ORG",
                         "loc": "LOC",
                         "time": "TIME"}

    map_datasets(datasets_to_map=de_datasets_to_map,
                 mapped_datasets=de_mapped_datasets, labels_mapping=de_labels_mapping)

    map_datasets(datasets_to_map=en_datasets_to_map,
                 mapped_datasets=en_mapped_datasets, labels_mapping=en_labels_mapping)

    map_datasets(datasets_to_map=es_datasets_to_map,
                 mapped_datasets=es_mapped_datasets, labels_mapping=es_labels_mapping)

    # ################################
    # Reduce datasets
    # ################################

    train_mapped_datasets = ["de_train_mapped.json",
                             "en_train_mapped.json", "es_train_mapped.json"]
    val_mapped_datasets = ["de_val_mapped.json",
                           "en_val_mapped.json", "es_val_mapped.json"]
    train_reduced_datasets = ["de_train_reduced.json",
                              "en_train_reduced.json", "es_train_reduced.json"]
    val_reduced_datasets = ["de_val_reduced.json",
                            "en_val_reduced.json", "es_val_reduced.json"]

    reduce_datasets(datasets_to_reduce=train_mapped_datasets,
                    reduced_datasets=train_reduced_datasets)

    reduce_datasets(datasets_to_reduce=val_mapped_datasets,
                    reduced_datasets=val_reduced_datasets)

    # ################################
    # Merge datasets
    # ################################

    merge_datasets(datasets_to_merge=train_reduced_datasets,
                   merged_dataset="train_joined.json")

    merge_datasets(datasets_to_merge=val_reduced_datasets,
                   merged_dataset="val_joined.json")


if __name__ == "__main__":
    main()
