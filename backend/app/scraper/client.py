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

# Заголовки, имитирующие обычный браузер
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Referer": "http://www.encar.com/",
}


class EncarClient:
    """HTTP-клиент для работы с внутренним API ENCAR.

    Реализует:
    - Retry с exponential backoff при сетевых ошибках
    - Rate limiting через паузы между запросами
    - Structured logging для отладки
    """

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
            wait=retry_state.next_action.sleep,
        ),
    )
    async def _fetch_page(
        self,
        client: httpx.AsyncClient,
        page: int,
    ) -> EncarSearchResponse:
        """Загрузка одной страницы результатов поиска."""
        params = {
            "count": settings.scraper_page_size,
            "page": page,
        }

        logger.debug(
            "Запрос страницы ENCAR", page=page, params=params
        )

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
        """Загрузка списка объявлений с пагинацией.

        Args:
            max_items: Максимальное количество объявлений для загрузки.

        Returns:
            Список спарсенных объявлений.
        """
        all_items: list[EncarRawItem] = []

        async with httpx.AsyncClient() as client:
            for page in range(1, settings.scraper_max_pages + 1):
                if len(all_items) >= max_items:
                    break

                try:
                    result = await self._fetch_page(client, page)
                except (
                    httpx.HTTPStatusError,
                    httpx.TransportError,
                ) as exc:
                    # После всех retry запрос не удался — идём дальше
                    logger.error(
                        "Не удалось загрузить страницу после retry",
                        page=page,
                        error=str(exc),
                    )
                    continue

                if not result.results:
                    logger.info(
                        "Пустая страница, завершаем пагинацию",
                        page=page,
                    )
                    break

                all_items.extend(result.results)

                # Rate limiting — пауза между запросами
                if page < settings.scraper_max_pages:
                    await asyncio.sleep(self._delay)

        # Обрезаем до max_items
        items = all_items[:max_items]
        logger.info(
            "Парсинг завершён",
            total_fetched=len(all_items),
            returned=len(items),
        )
        return items

    def build_photo_url(self, photo_path: str) -> str | None:
        """Формирование полного URL фотографии.

        ENCAR отдаёт относительный путь к фото, нужно собрать полный URL.
        Формат: https://ci.encar.com/carpicture01/{path}
        """
        if not photo_path:
            return None
        if photo_path.startswith("http"):
            return photo_path
        return f"{settings.encar_photo_base_url}/{photo_path.lstrip('/')}"

    def build_detail_url(self, encar_id: str) -> str:
        return f"{settings.encar_detail_url}?carid={encar_id}"
