import pytest
from unittest.mock import AsyncMock, patch

from app.scraper.schemas import EncarRawItem
from app.scraper.service import ScraperService


def make_raw_item(**overrides) -> EncarRawItem:
    """Хелпер для создания тестовых объявлений."""
    defaults = {
        "Id": "12345",
        "Manufacturer": "Hyundai",
        "Model": "Sonata",
        "Badge": "DN8",
        "BadgeDetail": "2.0",
        "Year": 2022,
        "Mileage": 35000,
        "Price": 2500,  # В 만원 (десятки тысяч вон)
        "FuelType": "Gasoline",
        "Photo": "carpicture01/pic123/12345_001.jpg",
    }
    defaults.update(overrides)
    return EncarRawItem.model_validate(defaults)


class TestScraperServiceMapping:
    """Тесты маппинга данных из ENCAR в нашу модель."""

    def setup_method(self) -> None:
        self.session = AsyncMock()
        self.service = ScraperService(self.session)

    def test_convert_price_standard(self) -> None:
        # Arrange — 2500 만원 = 25,000,000 KRW
        price_manwon = 2500

        # Act
        result = self.service._convert_price(price_manwon)

        # Assert — 25_000_000 * 0.00074 = 18_500
        assert result == 18500

    def test_convert_price_zero(self) -> None:
        assert self.service._convert_price(0) == 0

    def test_map_to_car_all_fields(self) -> None:
        # Arrange
        item = make_raw_item()

        # Act
        car_data = self.service._map_to_car(item)

        # Assert
        assert car_data["encar_id"] == "12345"
        assert car_data["brand"] == "Hyundai"
        assert car_data["model"] == "Sonata"
        assert car_data["year"] == 2022
        assert car_data["mileage_km"] == 35000
        assert car_data["price_krw"] == 25_000_000
        assert car_data["price_usd"] == 18500
        assert "ci.encar.com" in car_data["image_url"]
        assert "carid=12345" in car_data["detail_url"]

    def test_map_to_car_empty_photo(self) -> None:
        # Arrange
        item = make_raw_item(Photo="")

        # Act
        car_data = self.service._map_to_car(item)

        # Assert
        assert car_data["image_url"] is None

    @pytest.mark.parametrize(
        "price_manwon,expected_krw",
        [
            (100, 1_000_000),
            (3500, 35_000_000),
            (10000, 100_000_000),
        ],
    )
    def test_price_krw_calculation(
        self, price_manwon: int, expected_krw: int
    ) -> None:
        """ENCAR отдаёт цену в 만원, мы храним в полных вонах."""
        item = make_raw_item(Price=price_manwon)
        car_data = self.service._map_to_car(item)
        assert car_data["price_krw"] == expected_krw


class TestEncarRawItemParsing:
    """Тесты парсинга JSON-ответа ENCAR."""

    def test_valid_item(self) -> None:
        data = {
            "Id": "99999",
            "Manufacturer": "Kia",
            "Model": "K5",
            "Year": 2023,
            "Mileage": 12000,
            "Price": 1800,
        }
        item = EncarRawItem.model_validate(data)
        assert item.encar_id == "99999"
        assert item.manufacturer == "Kia"

    def test_item_with_missing_optional_fields(self) -> None:
        """Badge, BadgeDetail, FuelType, Photo — опциональные."""
        data = {
            "Id": "11111",
            "Manufacturer": "BMW",
            "Model": "3 Series",
            "Year": 2021,
            "Mileage": 50000,
            "Price": 4000,
        }
        item = EncarRawItem.model_validate(data)
        assert item.badge == ""
        assert item.photo == ""
