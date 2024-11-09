from .models import ItemInfo
from .text_parser import TextParser
from .types_ import ItemCategory
from .unificator import Unificator


class InfoParser:
    IMAGES_URL = "http://static.image.mihoyo.com/hsod2_webview/images/broadcast_top/equip_icon/png/"

    @classmethod
    def parse_info(cls, item_main_data: dict[str, str]) -> ItemInfo:
        id = cls.parse_id(item_main_data)
        title_id = title_id = cls.parse_title_id(item_main_data)
        title = cls.get_title(title_id)
        image_id = cls.parse_image_id(item_main_data)
        image_url = cls.get_image_url(image_id)
        damage_type = cls.parse_damage_type(item_main_data)
        rarity = cls.parse_rarity(item_main_data)

        item_info = ItemInfo(
            id, title_id, title, image_id, image_url, damage_type, rarity
        )

        return item_info

    @staticmethod
    def parse_id(item_main_data: dict[str, str]) -> int:
        id = int(item_main_data["DisplayNumber"])

        return id

    @staticmethod
    def parse_title_id(item_main_data: dict[str, str]) -> int:
        title_id = int(item_main_data["DisplayTitle"])

        return title_id

    @staticmethod
    def get_title(title_id: int) -> str:
        title = TextParser.parse_text(title_id)

        return title

    @staticmethod
    def parse_image_id(item_main_data: dict[str, str]) -> int:
        image_id = int(item_main_data["DisplayImage"])

        return image_id

    @classmethod
    def get_image_url(cls, image_id: int) -> str:
        trailing_zero = "0" * (3 - len(str(image_id)))
        image_url = f"{cls.IMAGES_URL}{trailing_zero}{image_id}.png"

        return image_url

    @staticmethod
    def parse_damage_type(item_main_data: dict[str, str]) -> str | None:
        damage_type = item_main_data.get("DamageType", "none")

        return Unificator.unificate_damage_type(damage_type)

    @staticmethod
    def parse_rarity(item_main_data: dict[str, str]) -> int:
        rarity = int(item_main_data["Rarity"])

        return rarity

    @staticmethod
    def parse_category(item_main_data: dict[str, str]) -> ItemCategory:
        category = item_main_data["Category"]

        return category
