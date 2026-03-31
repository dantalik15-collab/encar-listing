from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import (
    BrandsResponse,
    CarResponse,
    CarsListResponse,
    ScraperRunResponse,
)
from app.db.session import get_session
from app.scraper.service import ScraperService
from app.services.car_service import CarService

router = APIRouter(prefix="/api/v1", tags=["cars"])


@router.get("/cars", response_model=CarsListResponse)
async def list_cars(
    brand: str | None = Query(None, description="Фильтр по марке"),
    year_min: int | None = Query(None, ge=1990),
    year_max: int | None = Query(None, le=2030),
    price_max_usd: float | None = Query(None, ge=0),
    sort_by: str = Query("created_at", pattern="^(created_at|price_usd|year|mileage_km)$"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> CarsListResponse:
    service = CarService(session)
    cars, total = await service.get_cars(
        brand=brand,
        year_min=year_min,
        year_max=year_max,
        price_max_usd=price_max_usd,
        sort_by=sort_by,
        offset=offset,
        limit=limit,
    )
    return CarsListResponse(
        items=[CarResponse.model_validate(c) for c in cars],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/cars/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> CarResponse:
    service = CarService(session)
    car = await service.get_car_by_id(car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarResponse.model_validate(car)


@router.get("/brands", response_model=BrandsResponse)
async def list_brands(
    session: AsyncSession = Depends(get_session),
) -> BrandsResponse:
    service = CarService(session)
    brands = await service.get_brands()
    return BrandsResponse(brands=brands)


@router.post("/scraper/run", response_model=ScraperRunResponse)
async def run_scraper(
    max_items: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> ScraperRunResponse:
    """Ручной запуск парсинга (для демо и отладки)."""
    service = ScraperService(session)
    stats = await service.run(max_items=max_items)
    return ScraperRunResponse(**stats)
