#!/bin/bash
echo "=== Тестирование DevOps проекта ==="

cd /home/ubnt/devops-project

# 1. Активируем виртуальное окружение
echo "1. Активация виртуального окружения..."
source venv/bin/activate

# 2. Запускаем Flask приложение в фоне
echo "2. Запуск Flask приложения..."
python -m app &
FLASK_PID=$!
sleep 3

# 3. Проверяем работу
echo "3. Проверка эндпоинтов..."
curl -s http://localhost:5000/ | python -m json.tool
curl -s http://localhost:5000/health | python -m json.tool

# 4. Тестируем health_check.py
echo "4. Тестирование health_check.py (5 секунд)..."
timeout 5 python scripts/health_check.py || true

# 5. Тестируем clean_old_files.py
echo "5. Тестирование clean_old_files.py..."
mkdir -p /tmp/devops_test
touch /tmp/devops_test/file1.log
touch /tmp/devops_test/file2.tmp
touch -d "10 days ago" /tmp/devops_test/old_file.log

python scripts/clean_old_files.py /tmp/devops_test --extension=.log --days=7 --dry-run

# 6. Останавливаем Flask
echo "6. Остановка Flask..."
kill $FLASK_PID 2>/dev/null || true

echo "=== Тестирование завершено ==="
