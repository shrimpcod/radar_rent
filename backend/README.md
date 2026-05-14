# Бэкенд — Radar Rent

REST API сервер для управления объявлениями об аренде, пользователями и агентствами.
Также содержит планировщик парсера и WebSocket сервер для real-time обновлений.

---

## Стек технологий

| Технология | Назначение |
|---|---|
| FastAPI | HTTP фреймворк, автодокументация |
| SQLAlchemy (async) | ORM для работы с БД |
| PostgreSQL | База данных |
| Alembic | Миграции схемы БД |
| Pydantic v2 | Валидация данных, схемы запросов/ответов |
| APScheduler | Планировщик задач (запуск парсера) |
| python-jose | JWT токены |
| passlib + argon2 | Хеширование паролей |
| pydantic-settings | Конфигурация из .env |

---

## Структура проекта

```
backend/app/
├── main.py              # Точка входа, CORS, планировщик, lifespan
├── api/v1/
│   ├── __init__.py      # Регистрация всех роутеров
│   └── endpoints/       # Эндпоинты по ресурсам
│       ├── auth.py      # POST /auth/login
│       ├── leads.py     # GET /leads, GET /leads/count
│       ├── agencies.py  # CRUD /agencies
│       ├── users.py     # CRUD /users
│       ├── teams.py     # CRUD /teams
│       ├── team_members.py  # CRUD /team_members
│       ├── positions.py # CRUD /positions
│       └── ws.py        # WebSocket /ws
├── core/
│   ├── config.py        # Настройки из .env (Settings)
│   ├── security.py      # JWT, хеширование паролей, dependencies
│   └── ws_manager.py    # Менеджер WebSocket соединений
├── db/
│   └── session.py       # Движок БД, фабрика сессий, get_db()
├── models/              # SQLAlchemy модели (таблицы)
├── schemas/             # Pydantic схемы (валидация)
└── services/            # Бизнес-логика
```

---

## API эндпоинты

Базовый URL: `/api/v1`

| Метод | Путь | Описание |
|---|---|---|
| POST | `/auth/login` | Вход, возвращает JWT токен |
| GET | `/leads` | Список объявлений (skip, limit) |
| GET | `/leads/count` | Количество объявлений |
| GET/POST/PUT/DELETE | `/agencies` | CRUD агентств |
| GET/POST/PUT/DELETE | `/users` | CRUD пользователей |
| GET/POST/PUT/DELETE | `/teams` | CRUD команд |
| GET/POST/PUT/DELETE | `/team_members` | CRUD участников команд |
| GET/POST/DELETE | `/positions` | CRUD должностей |
| WS | `/ws` | WebSocket подключение |

Документация: `http://localhost:8000/api/docs` (Swagger UI)

---

## Ключевые архитектурные решения

### Lifespan — запуск планировщика

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    scheduler.add_job(
        parse_cian_tasks,
        trigger=IntervalTrigger(minutes=5, jitter=60),
    )
    await parse_cian_tasks()  # первый запуск сразу при старте
    yield
```

При старте приложения сразу запускается парсер, затем каждые 5 минут ± 60 секунд случайного jitter.
`jitter` нужен чтобы не нагружать сервер строго по расписанию и имитировать непредсказуемое поведение.

### Асинхронная БД

```python
engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

Все запросы к БД асинхронные — сервер не блокируется пока ждёт ответа от PostgreSQL.
`get_db()` — FastAPI dependency, автоматически закрывает сессию после запроса.

### Схемы Pydantic — валидация и сериализация

```python
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # создание схемы из SQLAlchemy модели
```

Все схемы наследуют `BaseSchema`. `from_attributes = True` позволяет передавать
SQLAlchemy объект напрямую в Pydantic — он сам извлечёт нужные поля.

```python
@router.get("/leads", response_model=List[LeadResponse])
async def get_all_leads(...):
    leads = await get_leads(db, skip=skip, limit=limit)
    return leads  # SQLAlchemy объекты → Pydantic автоматически
```

### JWT авторизация

```python
# Токен создаётся при логине
token = create_access_token({"sub": str(user.id)})

# Защищённые эндпоинты используют dependency
async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    payload = decode_access_token(token)
    user = await db.get(User, int(payload["sub"]))
    return user
```

Токен живёт 1440 минут (24 часа), задаётся в `.env`.
Пароли хешируются через `argon2` — современный безопасный алгоритм.

### WebSocket менеджер

```python
class ConnectionManager:
    async def connect(self, websocket: WebSocket)
    def disconnect(self, websocket: WebSocket)
    async def broadcast(self, data: dict)  # отправляет всем подключённым клиентам
```

Когда парсер сохраняет новый лид — вызывается `broadcast()`.
Все подключённые браузеры получают данные мгновенно без перезагрузки страницы.

---

## Модели БД (таблицы)

| Модель | Таблица | Описание |
|---|---|---|
| Lead | leads | Объявление об аренде |
| User | users | Пользователь системы |
| Agency | agencies | Агентство недвижимости |
| Team | teams | Команда внутри агентства |
| TeamMember | team_members | Участник команды + роль |
| Position | positions | Должность пользователя |
| Owner | owners | Собственник квартиры |
| LeadAction | lead_actions | Действия с лидом (звонки) |

---

## Конфигурация (.env)

```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
PROXIES=http://user:pass@host:port,...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
TELEGRAM_PROXY=http://127.0.0.1:10801
```

---

## Запуск

```bash
cd backend
alembic upgrade head        # применить миграции
py -3.12 -m venv venv # применятеся при установке проекта на комп
docker-compose up -d
./venv/Scripts/activate # для активации виртуального окружения
uvicorn app.main:app --reload
```

Сервер запускается на `http://localhost:8000`.
