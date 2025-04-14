from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import Reservation


class Table(Base):
    __tablename__ = "tables"
    name: Mapped[str] = mapped_column(unique=True)
    seats: Mapped[int]
    location: Mapped[str]

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan"
    )
