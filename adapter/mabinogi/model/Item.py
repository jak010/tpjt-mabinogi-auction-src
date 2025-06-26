from dataclasses import dataclass, asdict


@dataclass
class Item:
    auction_item_category: str
    item_name: str

    def to_dict(self):
        return asdict(self)
