from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения. Все значения читаются из .env файла."""

    # Приложение
    app_name: str = "Encar Listing"
    debug: bool = False

    # База данных
    database_url: str = (
        "postgresql+asyncpg://encar:encar@db:5432/encar"
    )

    # Парсер ENCAR
    encar_base_url: str = "http://api.encar.com/search/car/list/premium"
    encar_detail_url: str = "http://www.encar.com/dc/dc_cardetailview.do"
    encar_photo_base_url: str = "https://ci.encar.com"
    scraper_page_size: int = 20
    scraper_max_pages: int = 5
    scraper_delay_seconds: float = 1.5
    scraper_max_retries: int = 3

    # Планировщик
    scraper_cron_hour: int = 3
    scraper_cron_minute: int = 0

    # Курс валюты KRW -> USD (обновлять при необходимости)
    krw_to_usd_rate: float = 0.00074

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
