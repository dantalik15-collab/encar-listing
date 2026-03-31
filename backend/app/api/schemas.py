from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CarResponse(BaseModel):
    id: UUID
    encar_id: str
    brand: str
    model: str
    year: int
    mileage_km: int
    price_krw: int
    price_usd: float
    image_url: str | None
    detail_url: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CarsListResponse(BaseModel):
    items: list[CarResponse]
    total: int
    offset: int
    limit: int


class BrandsResponse(BaseModel):
    brands: list[str]


class ScraperRunResponse(BaseModel):
    inserted: int
    updated: int
    errors: int
