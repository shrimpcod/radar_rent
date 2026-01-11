# Описание фронтенда

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