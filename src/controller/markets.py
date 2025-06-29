from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter

from src.services.item_statistics_service import ItemStatisticsService
from src.services.market_service import MarketService
from .schema.market_schema import (
    MarketItemRequest,
    MarketItemResponse,
    ItemStatisticResponse
)

markets_router = APIRouter(tags=["MARKETS"])


@markets_router.get(
    path="/market/items",
    summary="입력 받은 Item 정보 반환",
    response_model=List[MarketItemResponse]
)
def get_items(
        request: MarketItemRequest = Depends(MarketItemRequest.as_param),
        service: MarketService = Depends(MarketService),
):
    auction_items = service.get_market_items(request)

    return MarketItemResponse.with_items(auction_items)


@markets_router.get(
    path="/market/statistics",
    summary="아이템 통계 정보 반환",
    response_model=ItemStatisticResponse
)
def get_item_statistics(
        item_name: str,
        service: ItemStatisticsService = Depends(ItemStatisticsService),
):
    statistics = service.get_item_statistics(item_name)
    return statistics
