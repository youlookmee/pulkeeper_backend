# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import transactions, reports, charts

app = FastAPI(
    title="PulKeeper Backend",
    description="API сервер для умного учета доходов и расходов (аналог Theo AI)",
    version="1.0.0",
)

# -----------------------------
# CORS (разрешаем доступ Flutter/React/Mobile App)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # можно ограничить при деплое
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Подключаем роутеры
# -----------------------------
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(charts.router, prefix="/api/charts", tags=["Charts"])


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "PulKeeper backend работает 🚀"
    }
