# app/routers/reports.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.database import get_session
from app import crud
from app.schemas import MonthlyReport, DailySummary, CategoryStat


router = APIRouter()


# ------------------------------------------------------------
# 📌 Месячный отчёт (доходы / расходы / баланс)
# ------------------------------------------------------------
@router.get("/month/{user_id}", response_model=MonthlyReport)
async def get_month_report_api(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_session)
):
    return await crud.get_month_report(db, user_id, year, month)


# ------------------------------------------------------------
# 📌 Дневной отчёт (доход / расход за день)
# ------------------------------------------------------------
@router.get("/day/{user_id}", response_model=DailySummary)
async def get_day_summary_api(
    user_id: int,
    date_value: date,
    db: AsyncSession = Depends(get_session)
):
    return await crud.get_day_summary(db, user_id, date_value)


# ------------------------------------------------------------
# 📌 Статистика по категориям за месяц
# ------------------------------------------------------------
@router.get("/categories/{user_id}", response_model=list[CategoryStat])
async def get_month_category_stats_api(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_session)
):
    return await crud.get_month_category_stats(db, user_id, year, month)
