from collections.abc import Hashable, Iterable
from pathlib import Path

from .tsvreader import TSVReader
from .utils import to_path


class DataLoader:
    @staticmethod
    def load_data(
        data_dir_path: str | Path,
        keys: Iterable[Hashable],
        data_file_names: Iterable[str | Path],
    ) -> dict[Hashable, TSVReader]:
        data = {}
        data_dir_path = to_path(data_dir_path)
        for key, data_file_name in zip(keys, data_file_names, strict=True):
            data[key] = TSVReader(data_dir_path / data_file_name)

        return data
