# 🍽️ Table Booking API
Простой и эффективный REST API для бронирования столиков в ресторане. \
Сервис позволяет управлять столиками и бронированиями с проверкой доступности временных слотов.

# 🚀 Технологии
Python 3.12

FastAPI - веб-фреймворк

SQLAlchemy - ORM

PostgreSQL - база данных

Alembic - миграции

Docker - контейнеризация

# 📚 API Endpoints
### 🪑 Столики
Метод	Эндпоинт	Описание
GET	/tables/	Получить список всех столиков \
POST	/tables/	Создать новый столик \
DELETE	/tables/{id}	Удалить столик \
Пример запроса POST /tables/ \

*json*
```
{
  "name": "VIP Booth",
  "seats": 4,
  "location": "У окна"
}
```
### 📅 Бронирования
Метод	Эндпоинт	Описание
GET	/reservations/	Получить список всех броней \
POST	/reservations/	Создать новую бронь \
DELETE	/reservations/{id}	Удалить бронь \
Пример запроса POST /reservations/ \

*json*
```
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2025-04-20T20:00:00",
  "duration_minutes": 120
}
```
Поддерживаемые форматы времени: "HH:MM", "DD.MM.YYYY HH:MM" или ISO 

# 🛠️ Установка и запуск
### Предварительные требования
Установленный Docker

Порт 8000 свободен

### Запуск проекта
Клонируйте репозиторий:

bash
```
git clone https://github.com/yourusername/restaurant-booking-api.git
cd restaurant-booking-api
```
Создайте файл .env в корне проекта (пример):

env
Copy
FASTAPI_CONFIG__DB__URL=postgresql+asyncpg://user:password@pg:5432/booking
FASTAPI_CONFIG__DB__ECHO=false
Запустите сервисы:

bash
Copy
docker compose up -d --build
Примените миграции:

bash
Copy
docker compose exec app alembic upgrade head
После успешного запуска API будет доступен по адресу:
🌐 http://localhost:8000

# 📝 Документация API
После запуска доступна интерактивная документация:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

# 🔍 Логирование
Логи приложения доступны:

В контейнере: booking_app/core/logs/booking_app.log

В хосте: ./logs/booking_app.log (после создания первого лога)

# 🏗️ Структура проекта
```
booking_app/
├── alembic/                  # Миграции Alembic
├── api/
│   ├── crud/
│   │   ├── reservations.py   # CRUD операции бронирований
│   │   └── tables.py         # CRUD операции столиков
│   └── v1/
│       ├── reservations.py   # Роутеры бронирований
│       └── tables.py         # Роутеры столиков
├── core/
│   ├── models/
│   │   ├── base.py           # Базовая модель SQLAlchemy
│   │   ├── db_helper.py      # Асинхронный движок и сессии
│   │   ├── reservation.py    # Модель бронирования
│   │   └── table.py          # Модель столика
│   ├── config.py             # Настройки приложения
│   └── logging.py            # Настройки логгирования
├── schemas/
│   ├── reservation.py        # Pydantic схемы бронирований
│   └── table.py              # Pydantic схемы столиков
├── .env.template             # Шаблон переменных окружения
├── .gitignore
├── alembic.ini               # Конфиг Alembic
├── docker-compose.yml
├── Dockerfile
├── main.py                   # Точка входа
├── poetry.lock
├── pyproject.toml
└── README.md
```