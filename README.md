### Задание 2 — API-пайплайн: Классификация тональности отзывов

##### Задание

Скрипт на Python, который читает отзывы о товарах из CSV-файла, отправляет каждый отзыв в языковую модель через API и получает обратно структурированный JSON с тональностью отзыва, темой и уровнем уверенности модели. Всё это автоматически сохраняется в итоговый CSV-файл.

В качестве LLM я использовала **Groq API** с моделью `llama-3.1-8b-instant`.

##### 

##### Как работает пайплайн

1. Скрипт открывает `reviews\_input.csv` и читает все отзывы
2. Каждый отзыв отправляется в API с инструкцией вернуть JSON
3. Ответ читает ответ модели и записывается в `reviews\_output.csv`

## 

##### Файлы в репозитории

```
API-Pipeline/
├── pipeline.py          # основной скрипт
├── reviews\_input.csv    # входные данные — 20 отзывов о товарах
├── reviews\_output.csv   # результат работы скрипта
└── README.md            # описание проекта
```

##### Запуск:

###### 1\. Установить зависимости

```bash
pip install requests
```

###### 2\. Получить API-ключ

Зарегистрироваться на [console.groq.com](https://console.groq.com), создать API-ключ и вставить его в скрипт в переменную `API\_KEY`.

###### 3\. Запустить скрипт

```bash
python pipeline.py
```

Скрипт обработает все отзывы и сохранит результат в `reviews\_output.csv`.

## 

###### Пример входных данных (reviews\_input.csv)

```
id,review\_text
1,"Absolutely love this product! It exceeded all my expectations."
2,"Terrible experience. The item broke after two days."
3,"It's okay, nothing special. Does what it's supposed to do."
```

###### Пример выходных данных (reviews\_output.csv)

```
id,review\_text,sentiment,topic,confidence,reason,status
1,"Absolutely love this product!...",positive,product quality,high,Strong positive language used,ok
2,"Terrible experience...",negative,product durability,high,Negative experience clearly described,ok
3,"It's okay...",neutral,general satisfaction,medium,Mixed or neutral language detected,ok
```

###### Формат JSON-ответа от модели

Модель возвращает JSON такого вида:

```json
{
  "sentiment": "positive",
  "topic": "product quality",
  "confidence": "high",
  "reason": "The review uses strongly positive language and expresses satisfaction."
}
```

##### Используемые технологии

* **Язык:** Python 3
* **API:** Groq (модель llama-3.1-8b-instant)
* **Входные данные:** CSV с 20 отзывами о товарах
* **Выходные данные:** CSV с результатами классификации по тональности

