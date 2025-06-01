from __future__ import annotations

import enum


class MCCCategory(enum.Enum):
    SUPERMARKET = "5411", "Продукти/Супермаркети"
    CAFE = "5814", "Кафе / Фастфуд"
    TAXI = "4121", "Таксі"
    FINANCE_P2P = "4829", "Фінанси / P2P"
    GROCERY = "5499", "Продукти / Магазини"
    RAILWAY = "4112", "Залізниця"
    TRAVEL = "4131", "Туризм"
    DELIVERY = "4215", "Доставка"
    BANKING = "6012", "Фінансові установи"
    PHARMACY = "5912", "Аптеки"
    COSMETICS = "5977", "Косметика"
    GAS = "5541", "АЗС"
    POSTAL = "7399", "Поштові послуги"
    OTHER = "", "Інше"

    def __new__(cls, code: str, description: str) -> MCCCategory:
        obj = object.__new__(cls)
        obj.code = code
        obj.description = description
        return obj

    @classmethod
    def from_code(cls, code: int | str) -> MCCCategory:
        code_str = str(code)
        for item in cls:
            if item.code == code_str:
                return item
        return cls.OTHER

    @classmethod
    def from_description(cls, description: str) -> MCCCategory:
        for item in cls:
            if item.description == description:
                return item
        return cls.OTHER


class Categorizer:

    @classmethod
    def categorize(cls, transactions: list[dict]) -> dict:
        categorized = dict()
        for tx in transactions:
            mcc = tx.get("mcc")
            category = MCCCategory.from_code(mcc).description
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(tx)
        return categorized