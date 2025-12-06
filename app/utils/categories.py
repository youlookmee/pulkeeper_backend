# app/utils/categories.py

# Основные категории (по стандарту финтех-приложений)
CATEGORIES = {
    "еда": [
        "еда", "food", "ресторан", "кафе", "cafe", "fastfood",
        "supermarket", "market", "продукт", "магазин еды"
    ],

    "покупки": [
        "магазин", "покупка", "store", "shop", "marketplace",
        "aliexpress", "olx", "korzinka", "carrefour", "uzum"
    ],

    "транспорт": [
        "такси", "yandex", "uber", "bolt", "автобус", "metro",
        "транспорт", "газ", "бензин", "azs", "zapravka"
    ],

    "развлечения": [
        "кино", "cinema", "игры", "game", "подписка", "music", "youtube",
        "netflix", "spotify", "kino", "entertainment"
    ],

    "связь": [
        "телефон", "мобиль", "uzmobile", "beeline", "ucell",
        "internet", "интернет"
    ],

    "коммуналка": [
        "коммунал", "квартплата", "газ", "электр", "свет", "вода",
        "energo", "kommunal"
    ],

    "прочее": []
}


# ------------------------------------------------------------
# 🔥 Функция: определение категории по тексту
# ------------------------------------------------------------
def detect_category(text: str) -> str:
    """
    Получает описание → возвращает подходящую категорию.
    """

    text = text.lower()

    for category, keywords in CATEGORIES.items():
        for k in keywords:
            if k in text:
                return category

    return "прочее"


# ------------------------------------------------------------
# 🔥 Нормализация категории (OCR может вернуть "food" → "еда")
# ------------------------------------------------------------
def normalize_category(category: str) -> str:
    """
    Приводим OCR или AI категорию к нашему стандарту.
    """

    if not category:
        return "прочее"

    c = category.lower().strip()

    # Прямое совпадение
    if c in CATEGORIES:
        return c

    # Поиск по ключевым словам
    for cat, keywords in CATEGORIES.items():
        if c in keywords:
            return cat

    return "прочее"
