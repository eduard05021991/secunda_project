FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY sql/ /app/sql/
# Install wait-for-it and postgresql-client
RUN apt-get update && apt-get install -y wait-for-it postgresql-client
CMD ["wait-for-it", "db:5432", "--timeout=120", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
