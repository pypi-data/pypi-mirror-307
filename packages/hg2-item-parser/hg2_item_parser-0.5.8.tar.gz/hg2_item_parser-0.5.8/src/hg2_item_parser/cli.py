from typing import Annotated

import typer

from .item_parser import ItemParser
from .utils import ask_overwrite_if_exists

app = typer.Typer()


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
