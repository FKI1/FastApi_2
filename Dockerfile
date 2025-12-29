FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Создаем директорию для данных и даем права
RUN mkdir -p /app/data && \
    chmod 777 /app/data

RUN useradd -m -u 1000 fastapi_user && \
    chown -R fastapi_user:fastapi_user /app
USER fastapi_user

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
