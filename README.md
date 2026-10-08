# Bio App

Backend учебной платформы: предметы → модули (теория, тест, практика) → прогресс пользователя.
FastAPI + async SQLAlchemy 2.0, JWT-авторизация.

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env            # задайте SECRET_KEY
alembic upgrade head           # применить миграции
python -m scripts.create_admin admin@example.com 'strong-password'
uvicorn app.main:app --reload   # документация: http://localhost:8000/docs
```

## Миграции (Alembic)

URL БД берётся из `DATABASE_URL` (см. `migrations/env.py`), драйвер асинхронный.

```bash
alembic upgrade head                              # применить все миграции
alembic revision --autogenerate -m "описание"     # создать миграцию по изменениям моделей
alembic downgrade -1                              # откатить одну миграцию
alembic check                                     # есть ли расхождения моделей и миграций
```

Новая модель должна импортироваться в `app/models/__init__.py`, иначе autogenerate её не увидит.
Тест `tests/test_migrations.py` падает, если модели и миграции разошлись.

## Проверки

```bash
pytest
ruff check . && ruff format --check .
mypy app
```

## Архитектура

- `app/models` — ORM: `User`, `Subject`, `Module` (тип + JSON-контент), `Progress` (лучший результат на пару пользователь+модуль).
- `app/modules` — стратегии типов модулей (`BaseModule`): валидация контента, скрытие ответов, оценка отправки. Новый тип = схема в `schemas/module_types`, класс в `modules/`, запись в `REGISTRY`.
- `app/services` — `module_executor` (диспетчеризация по типу), `progress_service` (запись попыток, сводка по предмету).
- `app/api/v1` — роуты: `auth`, `subjects`, `modules` (в т.ч. `POST /modules/{id}/submit`), `progress`, `admin`.
