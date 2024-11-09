import importlib.resources
import re
from typing import Literal

import requests

from .tsvreader import TSVReader


class TextParser:
    with importlib.resources.path(
        "hg2_item_parser.resources", "TextMap_aio.tsv"
    ) as resource_path:
        textmap = TSVReader(resource_path)
    en_re_url = "http://ggz.amaryllisworks.pw:18880/en_re"
    en_re: dict[str, str] = requests.get(en_re_url).json()

    @classmethod
    def parse_text(cls, text_id: str | int) -> str | Literal["No translation yet"]:
        text_en_re = cls.parse_text_en_re(text_id)
        text_textmap = cls.parse_text_textmap(text_id)

        return text_en_re or text_textmap or "No translation yet"

    @classmethod
    def parse_text_en_re(cls, text_id: str | int) -> str | None:
        text_en_re = cls.en_re.get(str(text_id))

        return text_en_re

    @classmethod
    def parse_text_textmap(cls, text_id: str | int) -> str | None:
        text_textmap = cls.textmap.get_row_by_column_value("TEXT_ID", text_id)
        if text_textmap is not None:
            return text_textmap["EN"]

        return None

    @staticmethod
    def fill_skill_description_template(
        skill_description_template: str,
        skill_max_lvl_values: list[float],
        skill_max_break_values: list[float],
    ) -> str:
        skill_description = re.sub(r"# ?!?ALB ?\(\d+\)", "", skill_description_template)
        skill_description = skill_description.replace("#n", "")
        skill_description = skill_description.replace(" %", "%")

        for i, skill_max_lvl_value, skill_max_break_value in zip(
            range(1, 7), skill_max_lvl_values, skill_max_break_values, strict=False
        ):
            if f"#{i}%" in skill_description:
                skill_max_lvl_value *= 100
                skill_max_break_value *= 100

            match = re.search(rf"([1-9]+)#{i}", skill_description)
            if match is not None:
                mul = match.group(1)
                skill_max_lvl_value *= int(mul)
                skill_max_break_value *= int(mul)
            else:
                mul = ""

            skill_fill_value = f"{skill_max_lvl_value:g}"
            if skill_max_lvl_value != skill_max_break_value:
                skill_fill_value += f"({skill_max_break_value:g})"

            skill_description = skill_description.replace(
                f"{mul}#{i}", skill_fill_value
            )

        skill_description = skill_description.strip()

        return skill_description
