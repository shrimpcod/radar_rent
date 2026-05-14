# Фронтенд — Radar Rent

Веб-интерфейс для работы с объявлениями об аренде жилья.
Интерфейс только для ПК, адаптива нет.

---

## Стек технологий

| Технология | Назначение |
|---|---|
| React 19 + TypeScript | UI и типизация |
| Vite | Сборщик, dev-сервер |
| Tailwind CSS v4 | Стилизация |
| React Router DOM | Маршрутизация |
| TanStack React Query v5 | Серверное состояние, кэширование |
| Zustand | Клиентское состояние |
| Axios | HTTP запросы к API |
| React Hook Form + Zod | Формы и валидация |
| React Icons | Иконки |

---

## Структура проекта

```
src/
├── api/           # Функции запросов к бэкенду
├── components/
│   ├── layout/    # AppLayout, Sidebar, Header
│   └── ui/        # Переиспользуемые компоненты (Modal, AdminTable)
├── features/      # Логика по фичам
│   ├── auth/      # Форма входа
│   ├── listings/  # Таблица объявлений, карточки статистики
│   └── admin/     # Панель суперадмина
├── pages/         # Тонкие страницы — компонуют фичи
├── router/        # Маршруты и защита роутов
├── store/         # Zustand сторы
├── types/         # TypeScript интерфейсы
└── utils/         # Утилиты (цвета)
```

---

## Маршруты

| Путь | Страница | Доступ |
|---|---|---|
| `/login` | Страница входа | Публичный |
| `/listings` | Таблица объявлений | Авторизованные |
| `/admin` | Панель суперадмина | Авторизованные |
| `/profile` | Профиль пользователя | Авторизованные |
| `/my_objects` | Объекты в работе | В разработке |
| `/clients` | База клиентов | В разработке |
| `/schedule` | График | В разработке |
| `*` | Редирект на `/listings` | — |

---

## Ключевые архитектурные решения

### Два вида состояния

**Клиентское состояние — Zustand:**
```ts
// Сессия пользователя — сохраняется в localStorage
const useAuthStore = create(persist(...))

// Состояние сайдбара (свёрнут/развёрнут) — сохраняется в localStorage
const useSidebarStore = create(persist(...))
```

**Серверное состояние — React Query:**
```ts
const { data, isLoading } = useQuery({
    queryKey: ['leads', page],
    queryFn: () => getLeads(skip, limit)
})
```

React Query кэширует данные, автоматически обновляет их при возврате на вкладку
(`refetchOnWindowFocus: true`), управляет состоянием загрузки и ошибок.

### Axios клиент с интерцептором

```ts
// src/api/client.ts
client.interceptors.request.use((config) => {
    const token = useAuthStore.getState().token
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})
```

JWT токен добавляется автоматически к каждому запросу.
`useAuthStore.getState()` используется вне компонентов — это правильный способ
обращаться к Zustand снаружи React дерева.

### WebSocket для real-time обновлений

```ts
useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/api/v1/ws")
    ws.onmessage = (event) => {
        const newLead = JSON.parse(event.data)
        setLeads(prev => [newLead, ...prev.slice(0, limit - 1)])
        // подсветка новой строки на 5 секунд
    }
    return () => ws.close()
}, [page])
```

Когда парсер находит новое объявление — оно мгновенно появляется в таблице
без перезагрузки страницы и подсвечивается зелёным на 5 секунд.

### Пагинация

```ts
queryFn: () => getLeads((page - 1) * limit, limit)
```

Бэкенд возвращает данные порциями через `skip/limit`.
Кнопки страниц реализованы как truncated pagination:
при большом количестве страниц показываются только крайние и соседние с текущей,
между ними — `...`

### Цвета вынесены в утилиту

```ts
// src/utils/colors.ts — менять цвета только здесь
export const colors = {
    text: '#DFE2FA',
    sidebarBg: 'linear-gradient(180deg, #232589B3 6%, #0A112A 100%)',
    activeItem: '#3D3FAA',
    contentBg: '#0A112A',
    loginText: '#232589',
}
```

---

## Слой API

Каждый файл в `src/api/` — набор функций для одного ресурса:

```
api/
├── client.ts      # Axios instance с интерцептором токена
├── auth.ts        # login()
├── listings.ts    # getLeads(), getLeadsCount(), downloadPhotos()
├── agencies.ts    # CRUD агентств
├── teams.ts       # CRUD команд
├── teamMembers.ts # CRUD участников команд
├── positions.ts   # CRUD должностей
└── users.ts       # CRUD пользователей
```

Функции принимают только данные, не знают ничего о компонентах.
Компоненты используют эти функции через React Query или напрямую.

---

## Страница объявлений (главная)

`ListingsPage` → `StatsCards` + `ListingsTable`

**Что происходит при загрузке:**
1. React Query делает `GET /api/v1/leads?skip=0&limit=12` → данные в таблице
2. React Query делает `GET /api/v1/leads/count` → количество страниц в пагинации
3. WebSocket подключается к `ws://localhost:8000/api/v1/ws` → слушает новые лиды

**Действия в таблице:**
- Открыть объявление на ЦИАН
- Скачать фото без водяных знаков (через `watermark_remover` сервис на порту 8001)
- Добавить в избранное (в разработке)
- Позвонить (в разработке)

---

## Панель суперадмина

`AdminPage` с вкладками:
- **Агентства** — полный CRUD
- **Должности** — создание и удаление
- **Пользователи** — полный CRUD, привязка к агентству и должности
- **Команды** — полный CRUD + управление участниками + смена роли участника

---

## Запуск

```bash
cd frontend
npm install
npm run dev     # dev-сервер на порту 5173
```

Переменные окружения (`frontend/.env`):
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
