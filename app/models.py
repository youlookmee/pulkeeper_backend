# app/models.py

from sqlalchemy import Column, Integer, BigInteger, String, Numeric, Text, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base


class Transaction(Base):
    """
    Основная таблица хранения транзакций.
    Аналог TheoAI — поддерживает:
    - доходы / расходы
    - категории
    - сумму
    - описание
    - дату транзакции
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)

    type = Column(String(10), nullable=False)  # "income" | "expense"
    amount = Column(Numeric(14, 2), nullable=False)

    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    tx_date = Column(Date, server_default=func.current_date())
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# В будущем можно добавить:
# class User(Base):
# class Budget(Base):
# class Goal(Base):
# class Subscription(Base):
