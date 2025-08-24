import dataclasses
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclasses.dataclass
class AuctionHistoryDto:
    item_name: str
    item_display_name: str
    item_count: int
    auction_price_per_unit: int
    date_auction_buy: str
    auction_buy_id: int
    item_option: None
    auction_item_category: Optional[str] = None  # JSON에 있는 값 대응

    def get_date_auction_buy(self):
        return datetime.strptime(self.date_auction_buy, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_date_auction_buy_kst(self):
        utc = datetime.strptime(self.date_auction_buy, "%Y-%m-%dT%H:%M:%S.%fZ")
        return utc.astimezone(tz=timezone(timedelta(hours=9)))

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"item_name={self.item_name}," \
               f"item_display_name={self.item_display_name}," \
               f"item_count={self.item_count}," \
               f"auction_price_per_unit={self.auction_price_per_unit}," \
               f"date_auction_buy={self.get_date_auction_buy_kst()})"
