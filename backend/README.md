# Описание бэкенда 

## 📁 Backend (Python + FastAPI) 
```bash
backend/
├── app/
│   ├── api/                    # API эндпоинты
│   │   ├── v1/                 # Версия API
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py    # Авторизация
│   │   │   │   ├── users.py   # Пользователи
│   │   │   │   ├── ???        # Основная логика радаров
│   │   │   │   ├── ???        # Логика аренды
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/                   # Ядро приложения
│   │   ├── config.py           # Конфигурация
│   │   ├── security.py         # Безопасность, JWT
│   │   └── __init__.py
│   ├── models/                 # SQLAlchemy/Pydantic модели
│   │   ├── user.py
│   │   ├── ???
│   │   ├── ???
│   │   └── __init__.py
│   ├── schemas/                # Pydantic схемы
│   │   ├── user.py
│   │   ├── ???
│   │   └── __init__.py
│   ├── services/               # Бизнес-логика
│   │   ├── user_service.py
│   │   ├── ???
│   │   └── ???
│   ├── db/                     # Работа с базой данных
│   │   ├── database.py
│   │   ├── repositories/ ???   # Репозитории (если используете)
│   │   └── migrations/         # Alembic миграции
│   ├── utils/                  # Вспомогательные функции
│   │   └── __init__.py
│   ├── tests/                  # Тесты бэкенда
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── conftest.py
│   ├── main.py                 # Точка входа
│   └── __init__.py
├── requirements/
│   ├── base.txt                # Основные зависимости
│   ├── dev.txt                 # Для разработки
│   └── prod.txt                # Для продакшена
├── alembic.ini                 # Конфиг миграций
├── Dockerfile                  # Dockerfile для бэкенда
├── pytest.ini                  # Конфиг тестов
└── .env.example                # Пример переменных окружения
```