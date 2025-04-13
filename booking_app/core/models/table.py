from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Table(Base):
    __tablename__ = "tables"
    name: Mapped[str] = mapped_column(unique=True)
    seats: Mapped[int]
    location: Mapped[str]
