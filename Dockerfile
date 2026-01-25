FROM python:3.11-slim
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app/ ./app/

# Открываем порт и запускаем приложение
EXPOSE 5000
CMD ["python", "-m", "app"]
