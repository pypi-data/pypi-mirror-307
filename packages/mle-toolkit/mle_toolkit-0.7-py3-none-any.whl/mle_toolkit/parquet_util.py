import typing as tp
from pathlib import Path

import pyarrow
import pyarrow.parquet as parquet
from tqdm import tqdm


# TODO: add unit test, then add to init file.

def total_rows(path: Path) -> int:
    dataset = parquet.ParquetDataset(path, use_legacy_dataset=False)
    return sum(p.count_rows() for p in dataset.fragments)


def split_into_partition(input_path: Path, output_folder: Path, partition_cols: tp.List[str],
                         batch_size: int = 10 ** 6):
    """
    Low RAM usage function for sharding parquet files
    """
    parquet_file = parquet.ParquetFile(input_path)
    total = total_rows(input_path) // batch_size
    for data in tqdm(parquet_file.iter_batches(batch_size=batch_size), total=total):
        parquet.write_to_dataset(
            pyarrow.Table.from_pandas(data.to_pandas()),
            root_path=output_folder,
            partition_cols=partition_cols,
        )
