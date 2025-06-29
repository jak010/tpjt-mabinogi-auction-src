from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter

from src.services.market_service import MarketService
from .schema.market_schema import (
    MarketItemRequest,
    MarketItemResponse
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
