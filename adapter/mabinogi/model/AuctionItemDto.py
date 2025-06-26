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

    def get_date_auction_expire_kst(self) -> datetime:
        """
        경매 만료 시간을 KST (UTC+9) datetime 객체로 반환합니다.
        """
        if isinstance(self.date_auction_expire, datetime):
            # 이미 datetime 객체인 경우, UTC+9로 변환 (naive datetime이라면 가정)
            # 실제로는 API 응답이 문자열이므로 이 경로는 거의 타지 않을 것입니다.
            return self.date_auction_expire.astimezone(timezone.utc) + timedelta(hours=9)
        else:
            # ISO 8601 문자열 파싱 후 UTC+9로 변환
            s = self.date_auction_expire.replace('Z', '+00:00')
            dt_utc = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
            return dt_utc + timedelta(hours=9)

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"item_name={self.item_name}," \
               f"item_display_name={self.item_display_name}," \
               f"item_count={self.item_count}," \
               f"auction_price_per_unit={self.auction_price_per_unit}," \
               f"date_auction_expire={self.get_date_auction_expire_kst().isoformat()})"
