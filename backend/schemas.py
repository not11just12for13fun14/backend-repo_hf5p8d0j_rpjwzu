from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

# Each class maps to a MongoDB collection with the lowercase class name

class Event(BaseModel):
    title: str
    description: str
    venue: str
    start_time: datetime
    end_time: datetime
    banner_url: Optional[str] = None
    categories: List[str] = []

    @field_validator('end_time')
    @classmethod
    def end_after_start(cls, v, values):
        start = values.get('start_time')
        if start and v <= start:
            raise ValueError('end_time must be after start_time')
        return v


class TicketType(BaseModel):
    event_id: str
    name: str
    price: float
    currency: str = "USD"
    quantity: int
    perks: List[str] = []


class Voucher(BaseModel):
    code: str
    discount_percent: float
    valid_from: datetime
    valid_to: datetime
    usage_limit: int = 0
    used: int = 0
    event_id: Optional[str] = None


class OrderItem(BaseModel):
    ticket_type_id: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    event_id: str
    email: str
    items: List[OrderItem]
    total: float
    payment_status: str = "pending"  # pending, paid, failed, refunded


class ScanEvent(BaseModel):
    qr: str
    device_id: Optional[str] = None
