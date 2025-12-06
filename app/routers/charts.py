# app/routers/charts.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from app.database import get_session
from app import crud
from app.schemas import ChartData


router = APIRouter()


# ------------------------------------------------------------
# 📊 Pie Chart: категории за месяц
# ------------------------------------------------------------
@router.get("/categories-pie/{user_id}", response_model=ChartData)
async def chart_categories_pie(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_session)
):
    stats = await crud.get_month_category_stats(db, user_id, year, month)

    labels = [item.category for item in stats]
    values = [item.amount for item in stats]

    return ChartData(labels=labels, values=values)


# ------------------------------------------------------------
# 📈 Line Chart: расходы по дням месяца
# ------------------------------------------------------------
@router.get("/daily-expenses/{user_id}", response_model=ChartData)
async def chart_daily_expenses(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_session)
):
    # Вычисляем количество дней в месяце
    from calendar import monthrange
    days_count = monthrange(year, month)[1]

    labels = []
    values = []

    for d in range(1, days_count + 1):
        day = date(year, month, d)
        summary = await crud.get_day_summary(db, user_id, day)
        labels.append(str(d))
        values.append(summary.expense)

    return ChartData(labels=labels, values=values)


# ------------------------------------------------------------
# 📉 Income vs Expense график
# ------------------------------------------------------------
@router.get("/income-expense/{user_id}", response_model=ChartData)
async def chart_income_expense(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_session)
):
    report = await crud.get_month_report(db, user_id, year, month)

    labels = ["Доход", "Расход"]
    values = [report.total_income, report.total_expense]

    return ChartData(labels=labels, values=values)
