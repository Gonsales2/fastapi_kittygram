# Необходимая установка
pip install sqlalchemy alembic aiosqlite fastapi uvicorn

# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить на одну миграцию
alembic downgrade -1

# Просмотреть историю
alembic history

# Показать текущую ревизию
alembic current

# Запуск проекта
uvicorn main:app --reload
