# app/utils/parser.py

import re
from typing import Optional, Dict


# ------------------------------------------------------------
# Функция: Парсинг текстовой строки транзакции
# ------------------------------------------------------------
def parse_transaction_text(text: str) -> Optional[Dict]:
    """
    Умеет распознавать транзакцию из строки вида:
      "20000 супермаркет"
      "1.5 млн зарплата"
      "50000 taxi"
      "100 000.50 магазин"

    Возвращает:
    {
        "amount": float,
        "category": str,
        "description": str,
        "type": "income" | "expense"
    }
    """

    text = text.lower().strip()

    # -------------------------------------
    # 1) Выделение числа (UZS)
    # -------------------------------------
    num_regex = r"[\d\s,.]+"
    num_match = re.search(num_regex, text)

    if not num_match:
        return None

    raw_amount = num_match.group(0)
    clean_amount = (
        raw_amount.replace(" ", "")
        .replace(",", "")
    )

    # случай "1.5 млн"
    if "млн" in text:
        try:
            clean_amount = float(clean_amount) * 1_000_000
        except:
            pass

    try:
        amount = float(clean_amount)
    except:
        return None

    # -------------------------------------
    # 2) Тип транзакции (доход/расход)
    # -------------------------------------
    income_keywords = ["зарп", "salary", "доход", "прибыль", "пополн", "income"]
    tx_type = "expense"
    if any(k in text for k in income_keywords):
        tx_type = "income"

    # -------------------------------------
    # 3) Описание и категория
    # -------------------------------------
    description = text.replace(raw_amount, "").strip()

    if not description:
        description = "транзакция"

    # Простая авто-категоризация
    category = detect_category(description)

    return {
        "amount": amount,
        "type": tx_type,
        "category": category,
        "description": description,
    }


# ------------------------------------------------------------
# Автоматическое определение категории по тексту
# ------------------------------------------------------------
def detect_category(description: str) -> str:
    description = description.lower()

    categories = {
        "еда": ["еда", "food", "ресторан", "cafe", "кафе", "sup", "market"],
        "транспорт": ["такси", "yandex", "uber", "каршеринг", "автобус"],
        "покупки": ["магазин", "покупка", "store", "shop"],
        "развлечения": ["кино", "игр", "развлеч"],
        "прочее": [],
    }

    for category, keywords in categories.items():
        for k in keywords:
            if k in description:
                return category

    return "прочее"
