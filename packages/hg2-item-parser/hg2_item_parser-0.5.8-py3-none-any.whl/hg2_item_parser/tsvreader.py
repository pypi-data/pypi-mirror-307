import csv
from pathlib import Path

from .utils import to_path


class TSVReader:
    def __init__(self, file_path: str | Path):
        self.file_path = to_path(file_path)
        self.data = self._load_data()

    def _load_data(self) -> list[dict[str, str]]:
        with self.file_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")

            return list(reader)

    def get_row_by_column_value(
        self, column_name: str, value: str | int | float
    ) -> dict[str, str] | None:
        for row in self.data:
            if row.get(column_name) == str(value):
                return row

        return None
