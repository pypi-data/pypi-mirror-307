from dataclasses import dataclass
from typing import Literal


class BaseItemModel:
    def __str__(self) -> str:
        return "\n".join(f"{name}: {value}" for name, value in self.__dict__.items())


@dataclass
class ItemInfo(BaseItemModel):
    id: int
    title_id: int
    title: str
    image_id: int
    image_url: str
    damage_type: str | None
    rarity: int


@dataclass
class ItemProperty(BaseItemModel):
    max_lvl: int


@dataclass
class WeaponProperty(ItemProperty):
    cost: int
    max_lvl_hp: int | float
    type: str | None
    max_lvl_damage: int | float
    max_lvl_ammo: int | float | Literal["∞"]
    max_lvl_atk_speed: float
    deploy_limit: int
    duration: float
    crit_rate: str


@dataclass
class CostumeProperty(ItemProperty):
    cost: int
    max_lvl_hp: int | float


@dataclass
class BadgeProperty(ItemProperty):
    cost: int


@dataclass
class PetProperty(ItemProperty):
    max_lvl_damage: int | float
    crit_rate: str
    base_sync: int | float
    max_sync: int | float


@dataclass
class ItemSkill(BaseItemModel):
    id: int
    damage_type: str | None
    title_id: int
    title: str
    description_template_id: int
    description_template: str
    description: str


@dataclass
class Item:
    info: ItemInfo
    property: ItemProperty
    skills: list[ItemSkill]

    def __str__(self) -> str:
        border = "-" * 15
        skills_str = f"\n{border}\n".join(str(skill) for skill in self.skills)

        return f"INFO\n{self.info}\n\nPROPERTY\n{self.property}\n\nSKILLS\n{skills_str or None}"
