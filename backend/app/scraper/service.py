from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models import Car
from app.scraper.client import EncarClient
from app.scraper.schemas import EncarRawItem

logger = get_logger(__name__)


class ScraperService:
    """Сервис парсинга: загрузка данных из ENCAR и сохранение в БД."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._client = EncarClient()

    def _convert_price(self, price_manwon: int) -> float:
        """Конвертация 만원 → USD."""
        price_full_krw = price_manwon * 10_000
        return round(price_full_krw * settings.krw_to_usd_rate)

    def _map_to_car(self, item: EncarRawItem) -> dict:
        price_full_krw = item.price_int * 10_000
        return {
            "encar_id": str(item.encar_id),
            "brand": EncarClient.translate_brand(item.manufacturer),
            "model": item.model,
            "year": item.year,
            "mileage_km": item.mileage_int,
            "price_krw": price_full_krw,
            "price_usd": self._convert_price(item.price_int),
            "image_url": self._client.build_photo_url(item),
            "detail_url": self._client.build_detail_url(
                str(item.encar_id)
            ),
        }

    async def _upsert_car(self, car_data: dict) -> str:
        stmt = select(Car).where(
            Car.encar_id == car_data["encar_id"]
        )
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing is None:
            car = Car(**car_data)
            self._session.add(car)
            return "inserted"

        existing.price_krw = car_data["price_krw"]
        existing.price_usd = car_data["price_usd"]
        existing.mileage_km = car_data["mileage_km"]
        existing.image_url = car_data["image_url"]
        return "updated"

    async def run(self, max_items: int = 100) -> dict:
        logger.info("Запуск парсинга ENCAR", max_items=max_items)

        items = await self._client.fetch_listings(max_items=max_items)
        stats = {"inserted": 0, "updated": 0, "errors": 0}

        for item in items:
            try:
                car_data = self._map_to_car(item)
                action = await self._upsert_car(car_data)
                stats[action] += 1
            except Exception:
                logger.exception(
                    "Ошибка обработки объявления",
                    encar_id=item.encar_id,
                )
                stats["errors"] += 1

        await self._session.commit()
        logger.info("Парсинг завершён", **stats)
        return stats
