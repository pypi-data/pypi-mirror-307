from pathlib import Path
from typing import Annotated

import typer

from .item_parser import ItemParser

app = typer.Typer()


def ask_overwrite_if_exists(file_path: str | Path) -> bool:
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if file_path.is_file():
        message = f"{file_path} is already exists, overwrite it? (y/n): "
        overwrite = input(message).lower() == "y"
    else:
        overwrite = True

    return overwrite


@app.command(help="Prints an item to a console")
def check(
    item_id: int, data_dir_path: Annotated[str, typer.Argument()] = "extracted"
) -> None:
    parser = ItemParser(data_dir_path)
    item = parser.parse_item(item_id)
    typer.echo(item)


@app.command(help="Parses items in range")
def parse_from_to(
    first_item_id: int,
    last_item_id: int,
    output_file_path: Annotated[str, typer.Argument()] = "parsed/items.txt",
    data_dir_path: Annotated[str, typer.Argument()] = "extracted",
) -> None:
    if ask_overwrite_if_exists(output_file_path):
        parser = ItemParser(data_dir_path)
        parser.parse_and_write_items_from_to(
            first_item_id, last_item_id, output_file_path, progressbar=True
        )


@app.command(help="Parses an item")
def parse(
    item_id: int,
    output_file_path: Annotated[str, typer.Argument()] = "parsed/items.txt",
    data_dir_path: Annotated[str, typer.Argument()] = "extracted",
) -> None:
    if ask_overwrite_if_exists(output_file_path):
        parser = ItemParser(data_dir_path)
        parser.parse_and_write_item(item_id, output_file_path)


def main() -> None:
    app()
