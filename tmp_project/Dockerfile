FROM python:3.11-slim

# Создаём рабочую директорию и даём права
WORKDIR /app
RUN chmod 777 /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Явно указываем порт и запускаем
ENV PORT=5000 \
    DB_PATH=/data/equipment_log.db \
    FLASK_DEBUG=false
EXPOSE 5000
CMD ["python", "app.py"]