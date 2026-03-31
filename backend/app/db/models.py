import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    encar_id: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage_km: Mapped[int] = mapped_column(Integer, nullable=False)
    price_krw: Mapped[int] = mapped_column(Integer, nullable=False)
    price_usd: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500))
    detail_url: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<Car {self.brand} {self.model} "
            f"({self.year}) ₩{self.price_krw:,}>"
        )
