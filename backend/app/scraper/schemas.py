from pydantic import BaseModel, Field


class EncarPhotoItem(BaseModel):
    location: str = ""
    ordering: float = 0.0


class EncarRawItem(BaseModel):
    """Схема одного объявления из ответа ENCAR API."""

    encar_id: str = Field(alias="Id")
    manufacturer: str = Field(alias="Manufacturer")
    model: str = Field(alias="Model")
    badge: str = Field(default="", alias="Badge")
    badge_detail: str = Field(default="", alias="BadgeDetail")
    form_year: str = Field(default="", alias="FormYear")
    year_raw: float = Field(default=0, alias="Year")
    mileage: float = Field(default=0, alias="Mileage")
    price: float = Field(default=0, alias="Price")
    fuel_type: str = Field(default="", alias="FuelType")
    photo: str = Field(default="", alias="Photo")
    photos: list[EncarPhotoItem] = Field(default_factory=list, alias="Photos")

    model_config = {"populate_by_name": True}

    @property
    def year(self) -> int:
        if self.form_year:
            return int(self.form_year)
        return int(self.year_raw) // 100

    @property
    def mileage_int(self) -> int:
        return int(self.mileage)

    @property
    def price_int(self) -> int:
        return int(self.price)

    @property
    def first_photo(self) -> str:
        """Первое фото из массива Photos или fallback на Photo."""
        if self.photos:
            sorted_photos = sorted(self.photos, key=lambda p: p.ordering)
            return sorted_photos[0].location
        return ""


class EncarSearchResponse(BaseModel):
    """Обёртка ответа поиска ENCAR."""

    count: int = Field(alias="Count", default=0)
    results: list[EncarRawItem] = Field(
        alias="SearchResults", default_factory=list
    )

    model_config = {"populate_by_name": True}
