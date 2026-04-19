# Задание 2 — API-пайплайн: Классификация тональности отзывов

### Описание задачи

Скрипт читает отзывы о товарах из CSV-файла, отправляет каждый отзыв в Claude (Anthropic API) и получает структурированный JSON-ответ с тональностью, темой и уверенностью модели. Результат сохраняется в выходной CSV-файл.

**Пайплайн:**

```
reviews\_input.csv → pipeline.py → Anthropic API (Claude) → reviews\_output.csv
```

### Структура проекта

```
task2/
├── pipeline.py          # основной скрипт
├── reviews\_input.csv    # входные данные (20 отзывов)
├── reviews\_output.csv   # результат работы скрипта
└── README.md            # этот файл
```

### Установка и запуск

##### 1\. Установить зависимости

```bash
pip install requests
```

##### 2\. Установить API-ключ

**Windows (PowerShell):**

```powershell
$env:ANTHROPIC\_API\_KEY="sk-ant-..."
```

**Mac / Linux:**

```bash
export ANTHROPIC\_API\_KEY="sk-ant-..."
```

##### 3\. Запустить скрипт

```bash
python pipeline.py
```

##### Пример входных данных ("reviews\_input.csv")

```
id,review\_text
1,"Absolutely love this product! It exceeded all my expectations."
2,"Terrible experience. The item broke after two days."
3,"It's okay, nothing special. Does what it's supposed to do."
```

##### Пример выходных данных ("reviews\_output.csv")

```
id,review\_text,sentiment,topic,confidence,reason,status
1,"Absolutely love this product!...",positive,product quality,high,Strong positive language used,ok
2,"Terrible experience...",negative,product durability,high,Negative experience described,ok
3,"It's okay...",neutral,general satisfaction,medium,Mixed or neutral language,ok
```

##### Формат JSON-ответа от Claude

```json
{
  "sentiment": "positive",
  "topic": "product quality",
  "confidence": "high",
  "reason": "The review uses strongly positive language and expresses satisfaction."
}
```

##### Используемые технологии

* **Язык:** Python 
* **API:** Anthropic Claude (claude-haiku-4-5)
* **Библиотеки:** `requests`, `csv`, `json`
* **Входные данные:** CSV (20 отзывов о товарах)
* **Выходные данные:** CSV с результатами классификации

