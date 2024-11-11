from datetime import datetime
from typing import List
from pydantic import BaseModel

class PaginatedResponse[T](BaseModel):
    items: List[T]
    total: int
    page: int
    per_page: int

class AdvertisementListItem(BaseModel):
    id: int
    cache_hash: str
    location_id: int
    source: str
    make: str
    link: str
    engine_capacity: int
    thumbnail: str
    engine_power: int
    price: int
    mileage: int
    price_currency: str
    model: str
    production_year: int
    transmission: str
    location_code: str
    fuel_type: str
    created_at: datetime