import csv
import json
import time
import requests

API_KEY = "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"
MODEL = "llama-3.1-8b-instant"
INPUT_FILE = "reviews_input.csv"
OUTPUT_FILE = "reviews_output.csv"

SYSTEM_PROMPT = """You are a sentiment analysis assistant.
Respond ONLY with a valid JSON object, no extra text, no markdown.
Format: {"sentiment": "positive" or "negative" or "neutral", "topic": "2-4 words", "confidence": "high" or "medium" or "low", "reason": "one sentence"}"""


def classify_review(review_text):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Review: " + review_text}
            ],
            "max_tokens": 200,
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)


def run_pipeline():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reviews = list(reader)

    print("Загружено отзывов: " + str(len(reviews)))
    print("-" * 60)

    results = []

    for row in reviews:
        review_id = row["id"]
        review_text = row["review_text"]

        print("[" + str(review_id) + "/" + str(len(reviews)) + "] Обрабатываю: " + review_text[:60] + "...")

        try:
            result = classify_review(review_text)
            results.append({
                "id": review_id,
                "review_text": review_text,
                "sentiment": result.get("sentiment", "unknown"),
                "topic": result.get("topic", ""),
                "confidence": result.get("confidence", ""),
                "reason": result.get("reason", ""),
                "status": "ok",
            })
            print("  -> " + str(result.get("sentiment")) + " | " + str(result.get("topic")) + " | " + str(result.get("confidence")))

        except Exception as e:
            error_detail = str(e)
            try:
                error_detail = e.response.text
            except Exception:
                pass
            print("  -> ОШИБКА: " + error_detail[:150])
            results.append({
                "id": review_id,
                "review_text": review_text,
                "sentiment": "error",
                "topic": "",
                "confidence": "",
                "reason": error_detail,
                "status": "error",
            })

        time.sleep(2)

    fieldnames = ["id", "review_text", "sentiment", "topic", "confidence", "reason", "status"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 60)
    print("Готово! Результат сохранён в " + OUTPUT_FILE)
    print("-" * 60)
    ok = [r for r in results if r["status"] == "ok"]
    for sentiment in ["positive", "negative", "neutral"]:
        count = sum(1 for r in ok if r["sentiment"] == sentiment)
        print("  " + sentiment + ": " + str(count) + " отзывов")
    print("  errors: " + str(len(results) - len(ok)))
    print("=" * 60)


run_pipeline()
