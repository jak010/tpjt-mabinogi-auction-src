from typing import List, Optional, Any, Dict

from fastapi import Query
from pydantic import BaseModel, Field

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
    date_auction_expire_kst: str # KST 시간 추가
    auction_item_category: str

    item_option: Any

    model_config = {
        "from_attributes": True,
        "validate_assignment": True
    }

    @classmethod
    def with_items(cls, items: List[AuctionItemDto]):
        return [
            cls(
                item_name=item.item_name,
                item_display_name=item.item_display_name,
                item_count=item.item_count,
                auction_price_per_unit=item.auction_price_per_unit,
                date_auction_expire=item.date_auction_expire,
                date_auction_expire_kst=item.get_date_auction_expire_kst().isoformat(), # KST 시간 추가
                auction_item_category=item.auction_item_category,
                item_option=item.item_option
            )
            for item in items
        ]


class ItemQuery(BaseModel):
    item_category: str = Field(..., description="아이템 카테고리")
    item_name: str = Field(..., description="아이템 이름")


class MarketChartRequest(BaseModel):
    items: List[ItemQuery] = Field(..., description="조회할 아이템 목록")

    @classmethod
    def as_param(cls,
                 item_categories: List[str] = Query(..., alias="item_category", description="아이템 카테고리 목록"),
                 item_names: List[str] = Query(..., alias="item_name", description="아이템 이름 목록"),
                 ):
        if len(item_categories) != len(item_names):
            raise ValueError("item_category와 item_name의 개수가 일치해야 합니다.")

        items = [
            ItemQuery(item_category=cat, item_name=name)
            for cat, name in zip(item_categories, item_names)
        ]
        return cls(items=items)


class ItemStatisticResponse(BaseModel):
    item_name: str = Field()
    total_items: int = Field()
    average_price: int = Field()
    time_based_average_price: int = Field()
    min_price: int = Field()
    max_price: int = Field()
    acquisition_rate_per_30_min: float = Field()
    acquisition_rate_per_hour: float = Field()
    profit_per_hour: float = Field()
    error: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }


class MarketChartResponse(BaseModel):
    item_data: Dict[str, List[MarketItemResponse]]

    model_config = {
        "populate_by_name": True
    }
