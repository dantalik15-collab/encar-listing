from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Car


class CarService:
    """Сервис для работы с каталогом автомобилей."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_cars(
        self,
        brand: str | None = None,
        year_min: int | None = None,
        year_max: int | None = None,
        price_max_usd: float | None = None,
        sort_by: str = "created_at",
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Car], int]:
        """Получение списка автомобилей с фильтрацией и пагинацией.

        Returns:
            Кортеж (список авто, общее количество).
        """
        stmt = select(Car)
        count_stmt = select(func.count(Car.id))

        if brand:
            stmt = stmt.where(Car.brand.ilike(f"%{brand}%"))
            count_stmt = count_stmt.where(
                Car.brand.ilike(f"%{brand}%")
            )
        if year_min:
            stmt = stmt.where(Car.year >= year_min)
            count_stmt = count_stmt.where(Car.year >= year_min)
        if year_max:
            stmt = stmt.where(Car.year <= year_max)
            count_stmt = count_stmt.where(Car.year <= year_max)
        if price_max_usd:
            stmt = stmt.where(Car.price_usd <= price_max_usd)
            count_stmt = count_stmt.where(
                Car.price_usd <= price_max_usd
            )

        # Сортировка
        sort_column = getattr(Car, sort_by, Car.created_at)
        stmt = stmt.order_by(sort_column.desc())

        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)
        cars = list(result.scalars().all())

        count_result = await self._session.execute(count_stmt)
        total = count_result.scalar() or 0

        return cars, total

    async def get_car_by_id(self, car_id: UUID) -> Car | None:
        stmt = select(Car).where(Car.id == car_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_brands(self) -> list[str]:
        """Получение уникальных марок для фильтра."""
        stmt = (
            select(Car.brand)
            .distinct()
            .order_by(Car.brand)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
