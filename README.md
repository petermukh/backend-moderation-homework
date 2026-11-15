# Сервис модерации объявлений

Учебный HTTP API на FastAPI для проверки объявлений по простому правилу.

## Установка и запуск

```bash
git clone https://github.com/petermukh/backend-moderation-homework.git
cd backend-moderation-homework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev
```

В Windows виртуальное окружение активируется командой `.venv\Scripts\activate`.
При запуске FastAPI создаёт документацию API по адресу `http://127.0.0.1:8000/docs`.

## Метод `POST /predict`

Метод принимает JSON-объект со всеми обязательными полями:

| Поле | Тип | Проверка |
| --- | --- | --- |
| `seller_id` | целое число | больше нуля |
| `is_verified_seller` | булево значение | строго `true` или `false` |
| `item_id` | целое число | больше нуля |
| `name` | строка | непустая после удаления пробелов по краям |
| `description` | строка | непустая после удаления пробелов по краям |
| `category` | целое число | больше нуля |
| `images_qty` | целое число | не меньше нуля |

Ответ содержит **только одно булево значение**, без объекта-обёртки:

- `true` — у объявления есть нарушение;
- `false` — нарушения нет.

Подтверждённый продавец всегда получает `false`. У неподтверждённого продавца
нарушение есть только тогда, когда нет изображений (`images_qty == 0`).
Остальные поля проверяются, но пока не влияют на решение.

Успешный запрос возвращает HTTP 200, некорректные входные данные — HTTP 400,
неожиданная ошибка при предсказании — HTTP 500.

Пример запроса:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"seller_id":1,"is_verified_seller":false,"item_id":2,"name":"Книга","description":"Книга в хорошем состоянии","category":3,"images_qty":0}'
```

Ответ: `true`.

## Устройство проекта и тесты

`routers.py` принимает HTTP-запрос и обрабатывает ошибку предсказания.
`services.py` содержит правило модерации. `repositories.py` хранит текущий
порог для числа изображений. `schemas.py` проверяет входные данные.

Тесты HTTP API находятся в `test_predict.py`, а тесты сервисного слоя —
в `test_service.py`. Запуск:

```bash
python -m pytest
```
