# 📊 PulKeeper Backend  
Интеллектуальная система учёта доходов и расходов.  
Backend уровня TheoAI: FastAPI + PostgreSQL + AI (GPT-4o Vision).

---

## 🚀 Возможности

### 💸 Управление транзакциями
- Добавление расходов и доходов
- Автокатегоризация
- История транзакций
- Редактирование / Удаление

### 📸 OCR — Распознавание чеков
- GPT-4o Mini Vision
- Автоматическое извлечение суммы, даты, описания
- Категоризация платежей

### 📊 Аналитика
- Месячные отчёты
- Дневные отчёты
- Категории по месяцам
- Графики (Pie, Line, Income vs Expense)
- Финансовый профиль пользователя

### 🔌 API (FastAPI)
- `/api/transactions/...`
- `/api/reports/...`
- `/api/charts/...`

---

## 🧱 Технологии

| Компонент | Используется |
|----------|--------------|
| Backend Framework | **FastAPI** |
| Database | **PostgreSQL** |
| ORM | **SQLAlchemy 2.x (async)** |
| AI OCR | **OpenAI GPT-4o mini Vision** |
| Server | **Docker + Uvicorn** |
| Deployment | Railway / Render / VPS |

---

## 📦 Структура проекта

