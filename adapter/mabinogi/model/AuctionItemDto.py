import dataclasses
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import List, Optional
import json


@dataclass
class AuctionItemDto:
    item_name: str
    item_display_name: str
    item_count: int
    auction_price_per_unit: int
    date_auction_expire: str
    auction_item_category: str

    item_option: Optional[List[dict]]

    def to_dict(self):
        # return asdict(self)
        return json.dumps(asdict(self), ensure_ascii=False)

    def get_date_auction_expire(self):
        return datetime.strptime(self.date_auction_expire, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_date_auction_expire_kst(self):

        if isinstance(self.date_auction_expire, datetime):
            return self.date_auction_expire
        else:
            s = self.date_auction_expire.replace('Z', '+00:00')  # Z → +00:00 으로 치환
            dt = datetime.fromisoformat(s)  # ISO8601 파싱
            return dt

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"item_name={self.item_name}," \
               f"item_display_name={self.item_display_name}," \
               f"item_count={self.item_count}," \
               f"auction_price_per_unit={self.auction_price_per_unit}," \
               f"date_auction_expire={self.get_date_auction_expire_kst()})"
