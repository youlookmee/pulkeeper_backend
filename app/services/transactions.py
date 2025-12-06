# app/services/transactions.py

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional, Dict

from app import crud
from app.schemas import TransactionCreate
from app.utils.parser import parse_transaction_text
from app.utils.ocr import extract_from_image


# ============================================================
# 🔥 1) Создание транзакции из ТЕКСТА
# ============================================================
async def create_from_text(db: AsyncSession, user_id: int, text: str):
    """
    Обрабатывает текст:
      "20000 такси"
      "1 млн зарплата"
      "50000 supermarket"
    """

    parsed = parse_transaction_text(text)
    if not parsed:
        return None

    tx = TransactionCreate(
        user_id=user_id,
        amount=parsed["amount"],
        type=parsed["type"],
        category=parsed["category"],
        description=parsed["description"],
        date=date.today(),
    )

    return await crud.create_transaction(db, tx)


# ============================================================
# 🔥 2) Создание транзакции из OCR (фото чека)
# ============================================================
async def create_from_receipt(db: AsyncSession, user_id: int, image_bytes: bytes):
    """
    Читает чек через OCR → создаёт транзакцию.
    """

    data = extract_from_image(image_bytes)
    if not data:
        return None

    tx = TransactionCreate(
        user_id=user_id,
        amount=data["amount"],
        type="expense",              # чек = всегда расход
        category=data["category"],
        description=data["description"],
        date=data.get("date") or date.today(),
    )

    return await crud.create_transaction(db, tx)


# ============================================================
# 🔥 3) Обновление транзакции (ручное)
# ============================================================
async def update_transaction(db: AsyncSession, tx_id: int, fields: Dict):
    """
    Обновляет: сумма, категория, описание, дата.
    """
    return await crud.update_transaction(db, tx_id, **fields)


# ============================================================
# 🔥 4) Удаление транзакции (отклонение)
# ============================================================
async def delete_transaction(db: AsyncSession, tx_id: int):
    return await crud.delete_transaction(db, tx_id)


# ============================================================
# 🔥 5) История транзакций
# ============================================================
async def get_history(db: AsyncSession, user_id: int, limit: int = 20):
    return await crud.get_history(db, user_id, limit)


# ============================================================
# 🔥 6) Месячный отчёт
# ============================================================
async def get_month_report(db: AsyncSession, user_id: int, year: int, month: int):
    return await crud.get_month_report(db, user_id, year, month)


# ============================================================
# 🔥 7) Дневной отчёт
# ============================================================
async def get_day_summary(db: AsyncSession, user_id: int, d: date):
    return await crud.get_day_summary(db, user_id, d)


# ============================================================
# 🔥 8) Категории за месяц (для Pie Chart)
# ============================================================
async def get_category_stats(db: AsyncSession, user_id: int, year: int, month: int):
    return await crud.get_month_category_stats(db, user_id, year, month)
