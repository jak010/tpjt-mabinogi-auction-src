import dataclasses
import datetime


@dataclasses.dataclass(order=True)
class Report:
    dated_at: str = None
    total_unit: int = None
    average_price: int = None
    low_price: int = None
    max_price: int = None

    def as_dict(self):
        return dataclasses.asdict(self)
