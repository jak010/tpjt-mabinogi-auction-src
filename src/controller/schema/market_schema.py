import json
from datetime import datetime
from typing import List, Optional, Any

from fastapi import Query
from pydantic import BaseModel

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


class MarketItemRequest(BaseModel):
    item_name: str
    item_category: str
    aggregate: int

    @classmethod
    def as_param(cls,
                 item_name: str = Query(default="고급 가죽"),
                 item_category: str = Query(default="천옷/방직"),
                 aggregate: int = Query(default=1),
                 ):
        return cls(
            item_name=item_name,
            item_category=item_category,
            aggregate=aggregate
        )


class MarketItemResponse(BaseModel):
    item_name: str
    item_display_name: str
    item_count: int
    auction_price_per_unit: int
    date_auction_expire: str
    auction_item_category: str

    item_option: Any

    model_config = {
        "from_attributes": True,
        "validate_assignment": True
    }

    @classmethod
    def with_items(cls, items: List[AuctionItemDto]):
        return [cls.model_validate(item) for item in items]
