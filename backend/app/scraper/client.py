import asyncio

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings
from app.core.logging import get_logger
from app.scraper.schemas import EncarRawItem, EncarSearchResponse

logger = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Referer": "https://www.encar.com/",
    "Origin": "https://www.encar.com",
}

# Маппинг корейских названий марок → английские
BRAND_MAP = {
    "현대": "Hyundai", "기아": "Kia", "제네시스": "Genesis",
    "쉐보레": "Chevrolet", "르노코리아": "Renault Korea",
    "KG모빌리티": "KG Mobility", "쌍용": "SsangYong",
    "BMW": "BMW", "벤츠": "Mercedes-Benz",
    "아우디": "Audi", "폭스바겐": "Volkswagen",
    "볼보": "Volvo", "토요타": "Toyota", "혼다": "Honda",
    "렉서스": "Lexus", "닛산": "Nissan", "포르쉐": "Porsche",
    "랜드로버": "Land Rover", "재규어": "Jaguar",
    "미니": "MINI", "푸조": "Peugeot", "시트로엥": "Citroen",
    "포드": "Ford", "링컨": "Lincoln", "지프": "Jeep",
    "캐딜락": "Cadillac", "테슬라": "Tesla",
    "마세라티": "Maserati", "페라리": "Ferrari",
    "람보르기니": "Lamborghini", "벤틀리": "Bentley",
    "롤스로이스": "Rolls-Royce", "맥라렌": "McLaren",
    "인피니티": "Infiniti", "스바루": "Subaru",
    "미쓰비시": "Mitsubishi", "로터스": "Lotus",
    "알파로메오": "Alfa Romeo", "피아트": "Fiat",
}


class EncarClient:
    """HTTP-клиент для работы с внутренним API ENCAR."""

    def __init__(self) -> None:
        self._delay = settings.scraper_delay_seconds

    @retry(
        stop=stop_after_attempt(settings.scraper_max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type(
            (httpx.HTTPStatusError, httpx.TransportError)
        ),
        before_sleep=lambda retry_state: get_logger(__name__).warning(
            "Retry запроса к ENCAR",
            attempt=retry_state.attempt_number,
        ),
    )
    async def _fetch_page(
        self,
        client: httpx.AsyncClient,
        page: int,
    ) -> EncarSearchResponse:
        """Загрузка одной страницы результатов поиска."""
        offset = page * settings.scraper_page_size
        params = {
            "count": "true",
            "q": "(And.Hidden.N.)",
            "inav": "|Metadata|Sort",
            "sr": f"|ModifiedDate|{offset}|{settings.scraper_page_size}",
        }

        logger.debug("Запрос страницы ENCAR", page=page, offset=offset)

        response = await client.get(
            settings.encar_base_url,
            params=params,
            headers=DEFAULT_HEADERS,
            timeout=15.0,
        )
        response.raise_for_status()

        data = response.json()
        parsed = EncarSearchResponse.model_validate(data)

        logger.info(
            "Страница загружена",
            page=page,
            items=len(parsed.results),
            total=parsed.count,
        )
        return parsed

    async def fetch_listings(
        self,
        max_items: int = 100,
    ) -> list[EncarRawItem]:
        all_items: list[EncarRawItem] = []

        async with httpx.AsyncClient() as client:
            for page in range(settings.scraper_max_pages):
                if len(all_items) >= max_items:
                    break

                try:
                    result = await self._fetch_page(client, page)
                except (
                    httpx.HTTPStatusError,
                    httpx.TransportError,
                ) as exc:
                    logger.error(
                        "Не удалось загрузить страницу",
                        page=page,
                        error=str(exc),
                    )
                    continue

                if not result.results:
                    logger.info("Пустая страница", page=page)
                    break

                all_items.extend(result.results)

                if page < settings.scraper_max_pages - 1:
                    await asyncio.sleep(self._delay)

        items = all_items[:max_items]
        logger.info(
            "Парсинг завершён",
            total_fetched=len(all_items),
            returned=len(items),
        )
        return items

    def build_photo_url(self, item: EncarRawItem) -> str | None:
        """Формирование полного URL первого фото."""
        photo_path = item.first_photo
        if not photo_path:
            return None
        if photo_path.startswith("http"):
            return photo_path
        return f"{settings.encar_photo_base_url}{photo_path}"

    def build_detail_url(self, encar_id: str) -> str:
        return f"{settings.encar_detail_url}?carid={encar_id}"

    @staticmethod
    def translate_brand(korean_name: str) -> str:
        return BRAND_MAP.get(korean_name, korean_name)
