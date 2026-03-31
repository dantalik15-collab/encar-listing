from pydantic import BaseModel, Field


class EncarRawItem(BaseModel):
    """Схема одного объявления из ответа ENCAR API.

    Поля маппятся из JSON-ответа ENCAR.
    Имена полей соответствуют ключам в API, поэтому используем alias.
    """

    encar_id: str = Field(alias="Id")
    manufacturer: str = Field(alias="Manufacturer")
    model: str = Field(alias="Model")
    badge: str = Field(default="", alias="Badge")
    badge_detail: str = Field(default="", alias="BadgeDetail")
    year: int = Field(alias="Year")
    mileage: int = Field(alias="Mileage")
    price: int = Field(alias="Price")
    fuel_type: str = Field(default="", alias="FuelType")
    photo: str = Field(default="", alias="Photo")

    model_config = {"populate_by_name": True}


class EncarSearchResponse(BaseModel):
    """Обёртка ответа поиска ENCAR."""

    count: int = Field(alias="Count", default=0)
    results: list[EncarRawItem] = Field(
        alias="SearchResults", default_factory=list
    )

    model_config = {"populate_by_name": True}
