from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .table import Table


class Reservation(Base):
    __tablename__ = "reservations"

    customer_name: Mapped[str]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    table: Mapped["Table"] = relationship(back_populates="reservations")
