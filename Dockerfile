FROM python:3.11-slim

WORKDIR /app

# Установка wait-for-it.sh
RUN apt-get update && apt-get install -y \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всей папки app в /app
COPY src/ .

# Копирование остальных файлов
COPY src/alembic.ini .
#COPY sql/ sql/
COPY .dockerignore .
COPY .gitignore .

CMD ["wait-for-it", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
