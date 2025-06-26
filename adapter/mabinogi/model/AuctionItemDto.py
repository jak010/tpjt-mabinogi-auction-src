import dataclasses
from datetime import datetime, timezone, timedelta
from typing import List


@dataclasses.dataclass
class AuctionItemDto:
    item_name: str
    item_display_name: str
    item_count: int
    auction_price_per_unit: int
    date_auction_expire: str
    auction_item_category: str

    item_option: List[dict]

    def get_date_auction_expire(self):
        return datetime.strptime(self.date_auction_expire, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_date_auction_expire_kst(self):
        utc = datetime.strptime(self.date_auction_expire, "%Y-%m-%dT%H:%M:%S.%fZ")
        return utc.astimezone(tz=timezone(timedelta(hours=9)))

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"item_name={self.item_name}," \
               f"item_display_name={self.item_display_name}," \
               f"item_count={self.item_count}," \
               f"auction_price_per_unit={self.auction_price_per_unit}," \
               f"date_auction_expire={self.get_date_auction_expire_kst()})"
