# Encar Listing

Парсер автомобилей с [Encar.com](https://www.encar.com) (крупнейшая автомобильная площадка Южной Кореи) + лендинг-витрина.

**Демо:** [cars.lunarion.ru](https://cars.lunarion.ru)

---

## Стек технологий

### Backend
- **Python 3.12** + **FastAPI**
- **SQLAlchemy 2.0** (async) + **Alembic**
- **PostgreSQL 16**
- **httpx** (async HTTP-клиент для парсинга)
- **tenacity** (retry с exponential backoff)
- **structlog** (structured logging)
- **APScheduler** (обновление данных раз в сутки)
- **Pydantic v2** (валидация данных)

### Frontend
- **Next.js 14** (App Router, standalone output)
- **TypeScript**
- **Tailwind CSS** (тёмная premium-тема)
- **TanStack Query** (data fetching + кэширование)

### Infrastructure
- **Docker Compose** (PostgreSQL + Backend + Frontend + Nginx)
- **Nginx** (reverse proxy, SSL termination)
- **Let's Encrypt** (SSL-сертификаты)

---

## Быстрый старт

### Требования
- Docker + Docker Compose

### Запуск

```bash
git clone https://github.com/dantalik15-collab/encar-listing.git
cd encar-listing
cp backend/.env.example backend/.env
docker compose up --build -d
```

Приложение доступно:
- **Лендинг:** http://localhost
- **API docs:** http://localhost/api/docs
- **Health check:** http://localhost/api/health

### Первый запуск парсера

После старта БД пустая. Запустите парсинг:

```bash
curl -X POST "http://localhost/api/v1/scraper/run?max_items=100"
```

Далее парсинг запускается автоматически каждый день в 03:00 UTC.

---

## API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/v1/cars` | Список авто (фильтры, пагинация, сортировка) |
| GET | `/api/v1/cars/{id}` | Детали автомобиля |
| GET | `/api/v1/brands` | Уникальные марки для фильтра |
| POST | `/api/v1/scraper/run` | Ручной запуск парсинга |
| GET | `/api/health` | Health check |

### Параметры фильтрации GET `/api/v1/cars`

| Параметр | Тип | Описание |
|----------|-----|----------|
| `brand` | string | Фильтр по марке (частичное совпадение) |
| `year_min` | int | Минимальный год |
| `year_max` | int | Максимальный год |
| `price_max_usd` | float | Максимальная цена в USD |
| `sort_by` | string | `created_at`, `price_usd`, `year`, `mileage_km` |
| `offset` | int | Смещение (пагинация) |
| `limit` | int | Лимит (1-100, по умолчанию 20) |

---

## Архитектура парсера

```
ENCAR API (api.encar.com/search/car/list/general)
    │  httpx async + retry (tenacity)
    │  rate limiting (1.5s между запросами)
    ▼
Pydantic валидация (EncarRawItem)
    │  маппинг полей (корейский → английский)
    │  конвертация KRW → USD
    ▼
Upsert в PostgreSQL
    ├── Новые → INSERT
    └── Существующие → UPDATE (цена, пробег)
```

**Ключевые особенности:**
- Прямое обращение к внутреннему API ENCAR (без Selenium/Playwright)
- Дедупликация по `encar_id` — повторный запуск не создаёт дубли
- Retry с exponential backoff (2s → 4s → 8s, до 3 попыток)
- Маппинг корейских названий марок в английские (현대 → Hyundai, 기아 → Kia)
- Structured logging (JSON в проде, цветной вывод в debug)
- Graceful error handling — ошибка одного объявления не останавливает парсинг
- Валидация данных через Pydantic

---

## Деплой на VPS

### 1. DNS
Добавить A-запись: `cars.lunarion.ru → IP VPS`

### 2. Запуск
```bash
ssh user@<vps-ip>
cd /opt
git clone https://github.com/dantalik15-collab/encar-listing.git
cd encar-listing
cp backend/.env.example backend/.env
docker compose up --build -d
curl -X POST "http://localhost/api/v1/scraper/run?max_items=100"
```

### 3. SSL (Let's Encrypt)
```bash
apt install -y certbot
certbot certonly --webroot -w ./certbot/www -d cars.lunarion.ru
docker compose restart nginx
```

---

## Структура проекта

```
encar-listing/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI роуты и схемы
│   │   ├── core/          # Конфиг, логирование
│   │   ├── db/            # Модели, сессия БД
│   │   ├── scraper/       # Парсер ENCAR (клиент, схемы, сервис)
│   │   └── services/      # Бизнес-логика
│   ├── tests/             # Тесты парсера
│   ├── alembic/           # Миграции БД
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js страницы
│   │   ├── components/    # UI-компоненты
│   │   └── lib/           # API-клиент, провайдеры
│   ├── Dockerfile
│   └── package.json
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```
