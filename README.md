# Радар Рент
Система парсинга новых объявлений долгосрочной аренды недвижимости

## Корневая структура проекта
```bash
radar_rent/
├── backend/              # Бэкенд на Python + FastAPI
├── frontend/            # Фронтенд на Vue.js
├── docs/                # Документация
├── scripts/             # Вспомогательные скрипты
├── docker/              # Docker-конфигурации (опционально)
├── .gitignore           # Git ignore для всего проекта
├── README.md            # Основная документация
├── docker-compose.yml   # Настройка контейнеров (опционально)
└── requirements.txt     # Python зависимости (или в backend/)
```

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

## Предпологаемая структура Frontend(Vue)
```bash
frontend/
├── public/                  # Статические файлы
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── assets/             # Статические ресурсы
│   │   ├── css/
│   │   ├── images/
│   │   └── fonts/
│   ├── components/         # Переиспользуемые компоненты
│   │   ├── common/        # Общие компоненты (кнопки, инпуты)
│   │   ├── layout/        # Компоненты layout (шапка, сайдбар)
│   │   └── ui/            # UI компоненты
│   ├── views/             # Страницы/вьюхи
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   ├── RadarListView.vue
│   │   ├── RadarDetailView.vue
│   │   └── RentView.vue
│   ├── router/            # Vue Router
│   │   └── index.js
│   ├── store/             # Vuex/Pinia хранилище
│   │   ├── modules/
│   │   │   ├── auth.js
│   │   │   ├── radar.js
│   │   │   └── rent.js
│   │   └── index.js
│   ├── services/          # API клиенты
│   │   ├── api.js         # Основной axios instance
│   │   ├── auth.js        # API для авторизации
│   │   ├── radar.js       # API для радаров
│   │   └── rent.js        # API для аренды
│   ├── composables/       # Vue 3 composables (опционально)
│   ├── utils/             # Вспомогательные функции
│   ├── App.vue            # Корневой компонент
│   └── main.js            # Точка входа
├── tests/                 # Тесты фронтенда
│   ├── unit/             # Юнит-тесты
│   └── e2e/              # E2E тесты
├── .env.development       # Переменные для разработки
├── .env.production        # Переменные для продакшена
├── vue.config.js         # Конфиг Vue CLI
├── package.json
├── Dockerfile            # Dockerfile для фронтенда
└── README.md             # Документация фронтенда
```
## Дополнительные папки в коре
```bash
docs/
├── api/                  # API документация
├── architecture/         # Архитектурные решения
├── deployment/          # Инструкции по деплою
└── user-guide/          # Пользовательская документация

scripts/
├── deploy.sh            # Скрипт деплоя
├── backup.sh            # Скрипт бэкапа
├── init-dev.sh          # Инициализация окружения
└── run-tests.sh         # Запуск всех тестов
```