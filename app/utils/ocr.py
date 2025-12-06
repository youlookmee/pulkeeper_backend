# app/utils/ocr.py

import base64
import json
import os
import re
from openai import OpenAI

from app.utils.parser import detect_category


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ------------------------------------------------------------
# 🔥 OCR-декодер чека через GPT-4o mini Vision
# ------------------------------------------------------------
def extract_from_image(image_bytes: bytes):
    """
    Возвращает строго:
    {
        "amount": float,
        "category": str,
        "description": str,
        "date": str
    }
    """

    # Кодируем фото в base64
    encoded = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
Ты — лучший в мире OCR ассистент для финансовых чеков (UZCARD/HUMO).
Твоя задача — извлечь точные данные.

Верни СТРОГО JSON:

{
  "amount": 0,
  "category": "",
  "description": "",
  "date": ""
}

Правила:
- amount: самое крупное число на чеке (UZS)
- category: выбери одну: "еда", "покупки", "развлечения", "транспорт", "прочее"
- description: кратко опиши платеж (одно предложение)
- date: найди дату в формате DD.MM.YYYY или YYYY-MM-DD. Если нет — ""
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Извлечь данные с чека"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded}"}
                ]
            }
        ]
    )

    raw = response.choices[0].message.content
    print("RAW OCR:\n", raw)

    # Ищем JSON
    try:
        json_match = re.search(r"\{[\s\S]*?\}", raw)
        if not json_match:
            raise ValueError("OCR JSON not found")

        data = json.loads(json_match.group(0))

    except Exception as e:
        print("OCR JSON ERROR:", e)
        return None

    # ---------------------------------------------------
    # 🔧 Коррекция суммы (если GPT ошибся)
    # ---------------------------------------------------
    if not data.get("amount") or float(data["amount"]) <= 0:
        numbers = re.findall(r"\d[\d\s,.]*", raw)
        cleaned_nums = []

        for n in numbers:
            nn = n.replace(" ", "").replace(",", "").replace(".", "")
            try:
                cleaned_nums.append(float(nn))
            except:
                pass

        if cleaned_nums:
            data["amount"] = max(cleaned_nums)

    # ---------------------------------------------------
    # Авто-категория (если пустая)
    # ---------------------------------------------------
    if not data.get("category"):
        data["category"] = detect_category(data.get("description", ""))

    # ---------------------------------------------------
    # Финальная очистка и возврат
    # ---------------------------------------------------
    return {
        "amount": float(data.get("amount", 0)),
        "category": data.get("category", "прочее"),
        "description": data.get("description", ""),
        "date": data.get("date", ""),
    }
