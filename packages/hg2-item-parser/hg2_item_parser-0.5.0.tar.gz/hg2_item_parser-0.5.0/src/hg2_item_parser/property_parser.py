from typing import Literal

from .info_parser import InfoParser
from .models import (
    BadgeProperty,
    CostumeProperty,
    ItemProperty,
    PetProperty,
    WeaponProperty,
)
from .unificator import Unificator


class PropertyParser:
    @classmethod
    def parse_property(cls, item_main_data: dict[str, str]) -> ItemProperty:
        property: ItemProperty
        match InfoParser.parse_category(item_main_data):
            case "weapon":
                property = cls.parse_weapon_property(item_main_data)
            case "costume":
                property = cls.parse_costume_property(item_main_data)
            case "badge":
                property = cls.parse_badge_property(item_main_data)
            case "pet":
                property = cls.parse_pet_property(item_main_data)

        return property

    @classmethod
    def parse_weapon_property(cls, item_main_data: dict[str, str]) -> WeaponProperty:
        max_lvl = cls.parse_max_lvl(item_main_data)
        cost = cls.parse_cost(item_main_data)
        max_lvl_hp = cls.parse_max_lvl_hp(item_main_data)
        type = cls.parse_weapon_type(item_main_data)
        max_lvl_damage = cls.parse_max_lvl_damage(item_main_data)
        max_lvl_ammo = cls.parse_max_lvl_ammo(item_main_data)
        max_lvl_atk_speed = cls.parse_max_lvl_atk_speed(item_main_data)
        deploy_limit = cls.parse_deploy_limit(item_main_data)
        duration = cls.parse_max_lvl_duration(item_main_data)
        crit_rate = cls.parse_crit_rate(item_main_data)

        weapon_property = WeaponProperty(
            max_lvl,
            cost,
            max_lvl_hp,
            type,
            max_lvl_damage,
            max_lvl_ammo,
            max_lvl_atk_speed,
            deploy_limit,
            duration,
            crit_rate,
        )

        return weapon_property

    @classmethod
    def parse_costume_property(cls, item_main_data: dict[str, str]) -> CostumeProperty:
        max_lvl = cls.parse_max_lvl(item_main_data)
        cost = cls.parse_cost(item_main_data)
        max_lvl_hp = cls.parse_max_lvl_hp(item_main_data)

        costume_property = CostumeProperty(max_lvl, cost, max_lvl_hp)

        return costume_property

    @classmethod
    def parse_badge_property(cls, item_main_data: dict[str, str]) -> BadgeProperty:
        max_lvl = cls.parse_max_lvl(item_main_data)
        cost = cls.parse_cost(item_main_data)

        badge_property = BadgeProperty(max_lvl, cost)

        return badge_property

    @classmethod
    def parse_pet_property(cls, item_main_data: dict[str, str]) -> PetProperty:
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_damage = cls.parse_max_lvl_damage(item_main_data)
        crit_rate = cls.parse_crit_rate(item_main_data)
        base_sync = cls.parse_base_sync(item_main_data)
        max_sync = cls.parse_max_up_sync(item_main_data)

        pet_property = PetProperty(
            max_lvl, max_lvl_damage, crit_rate, base_sync, max_sync
        )

        return pet_property

    @staticmethod
    def parse_max_lvl(item_main_data: dict[str, str]) -> int:
        max_lvl = int(item_main_data["MaxLv"])

        return max_lvl

    @staticmethod
    def parse_cost(item_main_data: dict[str, str]) -> int:
        cost = int(item_main_data["Cost"])

        return cost

    @staticmethod
    def parse_weapon_type(item_main_data: dict[str, str]) -> str | None:
        weapon_type = item_main_data["BaseType"]

        return Unificator.unificate_weapon_type(weapon_type)

    @staticmethod
    def parse_deploy_limit(item_main_data: dict[str, str]) -> int:
        deploy_limit = int(item_main_data["LimitedNumber"])

        return deploy_limit

    @staticmethod
    def parse_crit_rate(item_main_data: dict[str, str]) -> str:
        if InfoParser.parse_category(item_main_data) == "pet":
            crit_rate = item_main_data["initCritRate"]
        else:
            crit_rate = item_main_data["CriticalRate"]
        crit_rate = str(round(float(crit_rate) * 100, 1)) + "%"

        return crit_rate

    @classmethod
    def parse_max_lvl_hp(cls, item_main_data: dict[str, str]) -> int | float:
        base_hp = cls.parse_base_hp(item_main_data)
        hp_per_level = cls.parse_hp_per_lvl(item_main_data)
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_hp = cls._calculate_value_on_lvl(base_hp, hp_per_level, max_lvl)

        return max_lvl_hp

    @staticmethod
    def parse_base_hp(item_main_data: dict[str, str]) -> float:
        base_hp = float(item_main_data["HPBase"])

        return base_hp

    @staticmethod
    def parse_hp_per_lvl(item_main_data: dict[str, str]) -> float:
        hp_per_level = float(item_main_data["HPAdd"])

        return hp_per_level

    @classmethod
    def parse_max_lvl_damage(cls, item_main_data: dict[str, str]) -> int | float:
        base_damage = cls.parse_base_damage(item_main_data)
        damage_per_level = cls.parse_damage_per_lvl(item_main_data)
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_damage = cls._calculate_value_on_lvl(
            base_damage, damage_per_level, max_lvl
        )

        return max_lvl_damage

    @staticmethod
    def parse_base_damage(item_main_data: dict[str, str]) -> float:
        if InfoParser.parse_category(item_main_data) == "pet":
            base_damage = float(item_main_data["Attack"])
        else:
            base_damage = float(item_main_data["DamageBase"])

        return base_damage

    @staticmethod
    def parse_damage_per_lvl(item_main_data: dict[str, str]) -> float:
        if InfoParser.parse_category(item_main_data) == "pet":
            damage_per_lvl = float(item_main_data["Attack_Add"])
        else:
            damage_per_lvl = float(item_main_data["DamageAdd"])

        return damage_per_lvl

    @classmethod
    def parse_max_lvl_ammo(
        cls, item_main_data: dict[str, str]
    ) -> int | float | Literal["∞"]:
        base_ammo = cls.parse_base_ammo(item_main_data)
        ammo_per_level = cls.parse_ammo_per_lvl(item_main_data)
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_ammo = cls._calculate_value_on_lvl(base_ammo, ammo_per_level, max_lvl)

        return max_lvl_ammo if max_lvl_ammo != -1 else "∞"

    @staticmethod
    def parse_base_ammo(item_main_data: dict[str, str]) -> float:
        base_ammo = float(item_main_data["AmmoBase"])

        return base_ammo

    @staticmethod
    def parse_ammo_per_lvl(item_main_data: dict[str, str]) -> float:
        ammo_per_lvl = float(item_main_data["AmmoAdd"])

        return ammo_per_lvl

    @classmethod
    def parse_max_lvl_atk_speed(cls, item_main_data: dict[str, str]) -> float:
        base_atk_speed = cls.parse_base_atk_speed(item_main_data)
        atk_speed_per_lvl = cls.parse_atk_speed_per_lvl(item_main_data)
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_atk_speed = cls._calculate_value_on_lvl(
            base_atk_speed, atk_speed_per_lvl, max_lvl, 3
        )

        return max_lvl_atk_speed

    @staticmethod
    def parse_base_atk_speed(item_main_data: dict[str, str]) -> float:
        base_atk_speed = float(item_main_data["FireRateBase"])

        return base_atk_speed

    @staticmethod
    def parse_atk_speed_per_lvl(item_main_data: dict[str, str]) -> float:
        atk_speed_per_lvl = float(item_main_data["FireRateAdd"])

        return atk_speed_per_lvl

    @classmethod
    def parse_max_lvl_duration(cls, item_main_data: dict[str, str]) -> float:
        base_duration = cls.parse_base_duration(item_main_data)
        duration_per_lvl = cls.parse_duration_per_lvl(item_main_data)
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_duration = cls._calculate_value_on_lvl(
            base_duration, duration_per_lvl, max_lvl, 2
        )

        return max_lvl_duration

    @staticmethod
    def parse_base_duration(item_main_data: dict[str, str]) -> float:
        base_duration = float(item_main_data["CountDownTime"])

        return base_duration

    @staticmethod
    def parse_duration_per_lvl(item_main_data: dict[str, str]) -> float:
        duration_per_lvl = float(item_main_data["CountDownTimeAdd"])

        return duration_per_lvl

    @classmethod
    def parse_max_up_sync(cls, item_main_data: dict[str, str]) -> float:
        base_sync = cls.parse_base_sync(item_main_data)
        sync_per_up = cls.parse_sync_per_up(item_main_data)
        max_sync = cls.parse_max_sync(item_main_data)
        max_up_sync = base_sync + sync_per_up * max_sync

        return max_up_sync

    @staticmethod
    def parse_max_sync(item_main_data: dict[str, str]) -> int:
        max_sync = int(item_main_data["SynMaxLevel"])

        return max_sync

    @staticmethod
    def parse_base_sync(item_main_data: dict[str, str]) -> float:
        base_sync = int(item_main_data["SynInit"])

        return base_sync

    @staticmethod
    def parse_sync_per_up(item_main_data: dict[str, str]) -> float:
        sync_per_lvl = int(item_main_data["SynAdd"])

        return sync_per_lvl

    @staticmethod
    def _calculate_value_on_lvl(
        base_value: float, value_per_lvl: float, lvl: int, precision: int = 0
    ) -> float | int:
        value = round(base_value + value_per_lvl * (lvl - 1), precision)
        if precision == 0:
            value = int(value)

        return value
