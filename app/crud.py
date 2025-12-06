# app/crud.py

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional

from app.models import Transaction
from app.schemas import (
    TransactionCreate,
    MonthlyReport,
    DailySummary,
    CategoryStat
)


# ------------------------------------------------------------
# СОЗДАНИЕ ТРАНЗАКЦИИ
# ------------------------------------------------------------
async def create_transaction(db: AsyncSession, data: TransactionCreate) -> Transaction:
    tx = Transaction(
        user_id=data.user_id,
        amount=data.amount,
        type=data.type,
        category=data.category,
        description=data.description,
        tx_date=data.date or date.today(),
    )

    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx


# ------------------------------------------------------------
# ПОЛУЧЕНИЕ ИСТОРИИ (последние N транзакций)
# ------------------------------------------------------------
async def get_history(db: AsyncSession, user_id: int, limit: int = 20):
    q = (
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.id.desc())
        .limit(limit)
    )
    return (await db.execute(q)).scalars().all()


# ------------------------------------------------------------
# СТАТИСТИКА ПО КАТЕГОРИЯМ ЗА МЕСЯЦ
# ------------------------------------------------------------
async def get_month_category_stats(db: AsyncSession, user_id: int, year: int, month: int):
    q = (
        select(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .where(
            Transaction.user_id == user_id,
            func.extract('year', Transaction.tx_date) == year,
            func.extract('month', Transaction.tx_date) == month,
            Transaction.type == "expense"
        )
        .group_by(Transaction.category)
    )

    rows = (await db.execute(q)).all()

    total = sum(float(r[1]) for r in rows) or 1.0

    return [
        CategoryStat(
            category=r[0],
            amount=float(r[1]),
            percentage=round(float(r[1]) * 100 / total, 2)
        )
        for r in rows
    ]


# ------------------------------------------------------------
# СУММА ЗА ДЕНЬ
# ------------------------------------------------------------
async def get_day_summary(db: AsyncSession, user_id: int, _date: date):
    income_q = (
        select(func.sum(Transaction.amount))
        .where(
            Transaction.user_id == user_id,
            Transaction.tx_date == _date,
            Transaction.type == "income"
        )
    )

    expense_q = (
        select(func.sum(Transaction.amount))
        .where(
            Transaction.user_id == user_id,
            Transaction.tx_date == _date,
            Transaction.type == "expense"
        )
    )

    income = (await db.execute(income_q)).scalar() or 0
    expense = (await db.execute(expense_q)).scalar() or 0

    return DailySummary(
        date=_date,
        income=float(income),
        expense=float(expense)
    )


# ------------------------------------------------------------
# ОБЩИЙ ОТЧЁТ ЗА МЕСЯЦ
# ------------------------------------------------------------
async def get_month_report(db: AsyncSession, user_id: int, year: int, month: int):
    income_q = (
        select(func.sum(Transaction.amount))
        .where(
            Transaction.user_id == user_id,
            func.extract('year', Transaction.tx_date) == year,
            func.extract('month', Transaction.tx_date) == month,
            Transaction.type == "income"
        )
    )

    expense_q = (
        select(func.sum(Transaction.amount))
        .where(
            Transaction.user_id == user_id,
            func.extract('year', Transaction.tx_date) == year,
            func.extract('month', Transaction.tx_date) == month,
            Transaction.type == "expense"
        )
    )

    income = (await db.execute(income_q)).scalar() or 0
    expense = (await db.execute(expense_q)).scalar() or 0

    return MonthlyReport(
        month=f"{month:02}.{year}",
        total_income=float(income),
        total_expense=float(expense),
        net=float(income) - float(expense)
    )


# ------------------------------------------------------------
# ОБНОВЛЕНИЕ ТРАНЗАКЦИИ
# ------------------------------------------------------------
async def update_transaction(db: AsyncSession, tx_id: int, **fields):
    q = select(Transaction).where(Transaction.id == tx_id)
    tx = (await db.execute(q)).scalar_one_or_none()

    if not tx:
        return None

    for key, value in fields.items():
        setattr(tx, key, value)

    await db.commit()
    await db.refresh(tx)
    return tx


# ------------------------------------------------------------
# УДАЛЕНИЕ ТРАНЗАКЦИИ
# ------------------------------------------------------------
async def delete_transaction(db: AsyncSession, tx_id: int):
    q = select(Transaction).where(Transaction.id == tx_id)
    tx = (await db.execute(q)).scalar_one_or_none()

    if not tx:
        return False

    await db.delete(tx)
    await db.commit()
    return True
