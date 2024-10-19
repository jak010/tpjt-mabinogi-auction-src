import dataclasses


@dataclasses.dataclass
class Item:
    auction_item_category: str
    item_name: str
