from typing import List

from fastapi import Query, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

markets_router = APIRouter(tags=["MARKETS"])

from .schema.market_schema import MarketItemRequest, MarketItemResponse

from src.services.market_service import MarketService


class MarketItemController:

    @staticmethod
    @markets_router.get(
        path="/market/items",
        summary="입력 받은 Item 정보 반환",
        response_model=List[MarketItemResponse]

    )
    def get_items(
            request: MarketItemRequest = Depends(MarketItemRequest.as_param),
            service: MarketService = Depends(MarketService)
    ):
        auction_items = service.get_market_items(request)

        return MarketItemResponse.with_items(auction_items)
