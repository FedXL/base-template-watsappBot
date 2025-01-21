GNU nano 5.4                                                                    restart.sh
#!/bin/bash

# Переменная для контейнеров
COMPOSE_FILE="docker-compose.yml"

# 1. Остановка и удаление контейнеров
echo "Останавливаю и удаляю контейнеры..."
if docker-compose pull; then
    echo "Контейнеры успешно обновлены."
else
    echo "Ошибка при остановке и удалении контейнеров." >&2
    exit 1
fi
sleep 0.5


if docker-compose restart; then
    echo "Контейнеры успешно удалены."
else
    echo "Ошибка при остановке и удалении контейнеров." >&2
    exit 1
fi
# Задержка 0.5 секунды
sleep 0.5



# 2. Удаление конкретного образа

# 4. Проверка состояния контейнеров
echo "Проверка состояния контейнеров..."
docker-compose ps


docker-compose logs -f



