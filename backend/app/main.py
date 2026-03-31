from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.models import Base
from app.db.session import async_session_factory, engine
from app.scraper.service import ScraperService

logger = get_logger(__name__)
scheduler = AsyncIOScheduler()


async def scheduled_scrape() -> None:
    """Фоновая задача парсинга по расписанию."""
    logger.info("Запуск запланированного парсинга")
    async with async_session_factory() as session:
        service = ScraperService(session)
        stats = await service.run(max_items=100)
        logger.info("Запланированный парсинг завершён", **stats)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging(debug=settings.debug)
    logger.info("Запуск приложения", app_name=settings.app_name)

    # Создание таблиц (для разработки; в проде — Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Планировщик — парсинг раз в сутки
    scheduler.add_job(
        scheduled_scrape,
        CronTrigger(
            hour=settings.scraper_cron_hour,
            minute=settings.scraper_cron_minute,
        ),
        id="daily_scrape",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Планировщик запущен",
        cron=f"{settings.scraper_cron_hour}:{settings.scraper_cron_minute:02d}",
    )

    yield

    scheduler.shutdown()
    await engine.dispose()
    logger.info("Приложение остановлено")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://cars.lunarion.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
