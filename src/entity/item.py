import dataclasses


@dataclasses.dataclass
class MoneyItem:
    category: str
    name: str
    time_per_minute: int
    time_per_count: int
    is_searchable: bool
    location_id: int
