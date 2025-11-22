from dataclasses import dataclass
from datetime import datetime


@dataclass
class Location:
    location_id: int
    code: str
    name: str
    created_at: datetime
