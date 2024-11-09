from pathlib import Path

from .tsvreader import TSVReader


class DataLoader:
    @staticmethod
    def load_data(
        data_dir_path: str | Path, data_file_map: dict[str, str]
    ) -> dict[str, TSVReader]:
        data = {}
        data_dir_path = Path(data_dir_path)
        for name, data_file_name in data_file_map.items():
            data[name] = TSVReader(data_dir_path / data_file_name)

        return data
