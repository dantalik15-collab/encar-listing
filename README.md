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
# Клонировать репозиторий
git clone https://github.com/<your-username>/encar-listing.git
cd encar-listing

# Скопировать env-файл
cp backend/.env.example backend/.env

# Запустить все сервисы
docker compose up --build -d

# Проверить что всё работает
curl http://localhost/api/health
# {"status": "ok"}
```

Приложение доступно:
- **Лендинг:** http://localhost
- **API docs:** http://localhost/api/docs
- **Health check:** http://localhost/api/health

### Первый запуск парсера

После старта БД пустая. Запустите парсинг вручную:

```bash
curl -X POST "http://localhost/api/v1/scraper/run?max_items=100"
```

Или через Swagger UI: http://localhost/api/docs → POST `/api/v1/scraper/run`

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
ENCAR API (api.encar.com)
    ↓ httpx async + retry (tenacity)
    ↓ rate limiting (1.5s между запросами)
Pydantic валидация (EncarRawItem)
    ↓ маппинг полей + конвертация KRW → USD
Upsert в PostgreSQL
    ├── Новые → INSERT
    └── Существующие → UPDATE (цена, пробег)
```

**Ключевые особенности:**
- Дедупликация по `encar_id` — повторный запуск не создаёт дубли
- Retry с exponential backoff (2s → 4s → 8s → ..., до 3 попыток)
- Structured logging (JSON в проде, цветной вывод в debug)
- Graceful error handling — ошибка одного объявления не останавливает весь парсинг
- Валидация данных через Pydantic — "грязные" записи отбрасываются

---

## Деплой на VPS

### 1. DNS

Добавить A-запись: `cars.lunarion.ru → <IP вашего VPS>`

### 2. Первый запуск

```bash
ssh user@<vps-ip>
git clone <repo> && cd encar-listing
cp backend/.env.example backend/.env
docker compose up --build -d
```

### 3. SSL (Let's Encrypt)

```bash
# Установить certbot
sudo apt install certbot

# Получить сертификат
sudo certbot certonly --webroot \
  -w ./certbot/www \
  -d cars.lunarion.ru

# Раскомментировать HTTPS-блок в nginx/nginx.conf
# Перезапустить nginx
docker compose restart nginx
```

---

## Разработка

```bash
# Backend (без Docker)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend (без Docker)
cd frontend
npm install
npm run dev
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
│   │   ├── scraper/       # Парсер ENCAR
│   │   └── services/      # Бизнес-логика
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
