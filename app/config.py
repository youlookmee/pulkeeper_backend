# app/config.py

import os
from dotenv import load_dotenv

# Загружаем .env файл (локально)
load_dotenv()

# ---------------------------------------------------------
# 🔐 БАЗОВЫЕ НАСТРОЙКИ
# ---------------------------------------------------------

# 1) Ключ API для будущего OCR, AI и т.д.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2) Подключение к базе данных (Railway предоставляет через DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не найден! Добавьте его в переменные окружения Railway или .env")

# ---------------------------------------------------------
# 🌍 РЕЖИМ РАБОТЫ
# ---------------------------------------------------------
ENVIRONMENT = os.getenv("ENV", "development")

DEBUG = ENVIRONMENT == "development"

# ---------------------------------------------------------
# 🚀 Глобальные параметры приложения
# ---------------------------------------------------------
APP_NAME = "PulKeeper Backend"
VERSION = "1.0.0"

