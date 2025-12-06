# app/schemas.py

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


# ------------------------------------------------------------
# БАЗОВАЯ СХЕМА ТРАНЗАКЦИИ
# ------------------------------------------------------------
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма в UZS")
    category: str = Field(..., min_length=1)
    description: Optional[str] = None
    type: str = Field(..., regex="^(income|expense)$")
    date: Optional[date] = None


# ------------------------------------------------------------
# СХЕМА ДЛЯ СОЗДАНИЯ ТРАНЗАКЦИИ
# ------------------------------------------------------------
class TransactionCreate(TransactionBase):
    user_id: int = Field(..., description="Telegram user id")


# ------------------------------------------------------------
# СХЕМА ВОЗВРАТА ТРАНЗАКЦИИ КЛИЕНТУ
# ------------------------------------------------------------
class TransactionResponse(TransactionBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True


# ------------------------------------------------------------
# СХЕМЫ ОТЧЁТОВ
# ------------------------------------------------------------
class MonthlyReport(BaseModel):
    month: str
    total_income: float
    total_expense: float
    net: float


class DailySummary(BaseModel):
    date: date
    income: float
    expense: float


class CategoryStat(BaseModel):
    category: str
    amount: float
    percentage: float


class ChartData(BaseModel):
    labels: list[str]
    values: list[float]
