# app/services/stats.py

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Dict, List

from app import crud
from app.schemas import CategoryStat


# ====================================================================
# 🔥 1) Сумма доходов / расходов за период
# ====================================================================
async def get_period_totals(
    db: AsyncSession,
    user_id: int,
    start: date,
    end: date
):
    total_income = 0
    total_expense = 0

    # получаем за каждый день
    d = start
    while d <= end:
        summary = await crud.get_day_summary(db, user_id, d)
        total_income += summary.income
        total_expense += summary.expense
        d = date.fromordinal(d.toordinal() + 1)

    return {
        "income": total_income,
        "expense": total_expense,
        "net": total_income - total_expense,
    }


# ====================================================================
# 🔥 2) Топ категорий (ТОП-5) за месяц
# ====================================================================
async def get_top_categories(
    db: AsyncSession,
    user_id: int,
    year: int,
    month: int,
    limit: int = 5,
):
    stats = await crud.get_month_category_stats(db, user_id, year, month)
    stats_sorted = sorted(stats, key=lambda x: x.amount, reverse=True)
    return stats_sorted[:limit]


# ====================================================================
# 🔥 3) Средний расход пользователя за день
# ====================================================================
async def get_daily_average_expense(
    db: AsyncSession, user_id: int, year: int, month: int
):
    from calendar import monthrange

    days = monthrange(year, month)[1]

    total_expense = 0

    for d in range(1, days + 1):
        summary = await crud.get_day_summary(db, user_id, date(year, month, d))
        total_expense += summary.expense

    return round(total_expense / days, 2)


# ====================================================================
# 🔥 4) Финансовый профиль пользователя (будет использоваться AI)
# ====================================================================
async def get_financial_profile(
    db: AsyncSession, user_id: int, year: int, month: int
) -> Dict:
    monthly = await crud.get_month_report(db, user_id, year, month)
    top_categories = await get_top_categories(db, user_id, year, month)
    avg = await get_daily_average_expense(db, user_id, year, month)

    return {
        "report": monthly,
        "top_categories": top_categories,
        "daily_average_expense": avg,
    }
