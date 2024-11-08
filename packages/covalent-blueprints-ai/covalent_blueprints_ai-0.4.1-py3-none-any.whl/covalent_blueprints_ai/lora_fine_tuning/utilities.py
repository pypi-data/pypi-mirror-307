# Copyright 2024 Agnostiq Inc.
"""Utilities for AI Recipes."""
from pathlib import Path
from typing import Optional, Union


def load_local_dataset_from_file(
    local_dataset: Union[str, Path], split: Optional[str] = None
):
    """Load a local dataset from a file into a Dataset object."""

    try:
        from datasets import Dataset
    except ImportError as e:
        raise RuntimeError(
            "The `datasets` package is required to fine-tune on local data. "
            "Please run `pip install datasets` to install it."
        ) from e

    local_dataset = Path(local_dataset).expanduser().absolute()
    local_dataset_str = str(local_dataset)
    if local_dataset.name.endswith(".csv"):
        data = Dataset.from_csv(local_dataset_str, split=split, keep_in_memory=True)
    elif local_dataset.name.endswith(".json"):
        data = Dataset.from_json(local_dataset_str, split=split, keep_in_memory=True)
    elif local_dataset.name.endswith(".txt"):
        data = Dataset.from_file(local_dataset_str, split=split, in_memory=True)
    elif local_dataset.name.endswith(".parquet"):
        data = Dataset.from_parquet(local_dataset_str, split=split, keep_in_memory=True)
    else:
        raise ValueError("Unsupported local dataset file format.")

    return data
