from datetime import datetime, timedelta
import re
from pydantic import BaseModel, Field, field_validator


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    table_id: int
    # "HH:MM", "DD.MM.YYYY HH:MM" или ISO формат "2025-04-14T20:30:00Z"
    reservation_time: datetime
    duration_minutes: int

    @field_validator('reservation_time', mode='before')
    def parse_human_time(cls, value):
        if isinstance(value, datetime):
            return value.replace(tzinfo=None)

        if isinstance(value, str):
            if re.match(r'^\d{1,2}:\d{2}$', value):
                today = datetime.now().date()
                hours, minutes = map(int, value.split(':'))
                return datetime.combine(today, datetime.min.time()) + timedelta(hours=hours, minutes=minutes)

            elif re.match(r'^\d{2}\.\d{2}\.\d{4} \d{1,2}:\d{2}$', value):
                return datetime.strptime(value, '%d.%m.%Y %H:%M')

            try:
                dt = datetime.fromisoformat(value)
                return dt.replace(tzinfo=None)
            except ValueError:
                pass

        raise ValueError(
            'Неправильный формат времени. Используйте: '
            '"HH:MM", "DD.MM.YYYY HH:MM" или ISO формат'
        )


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int

    class Config:
        from_attributes = True
