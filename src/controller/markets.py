from typing import List, Dict

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.services.market_service import MarketService
from .schema.market_schema import (
    MarketItemRequest,
    MarketItemResponse,
    MarketChartRequest,
    MarketChartResponse
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
    path="/market/chart-data",
    summary="여러 아이템의 가격 변동 추이 및 통계, 추천 정보 반환",
    response_model=MarketChartResponse
)
def get_chart_data(
        request: MarketChartRequest = Depends(MarketChartRequest.as_param),
        service: MarketService = Depends(MarketService)
):
    item_data_map: Dict[str, List[MarketItemResponse]] = {}
    raw_auction_items_map: Dict[str, List[AuctionItemDto]] = {}

    for item_query in request.items:
        try:
            market_item_request = MarketItemRequest(
                item_name=item_query.item_name,
                item_category=item_query.item_category,
                aggregate=1  # 이 엔드포인트에서는 집계 로직을 MarketService 내부에서 처리하므로 1로 고정
            )
            auction_items = service.get_market_items(market_item_request)
            item_data_map[item_query.item_name] = auction_items
            raw_auction_items_map[item_query.item_name] = auction_items
        except Exception as e:
            # 특정 아이템에 대한 데이터 로드 실패 시에도 다른 아이템은 계속 처리
            print(f"Error fetching data for {item_query.item_name}: {e}")
            item_data_map[item_query.item_name] = []  # 실패한 아이템은 빈 리스트로 처리
            raw_auction_items_map[item_query.item_name] = []

    if not item_data_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="요청된 아이템에 대한 데이터를 찾을 수 없습니다."
        )

    statistics_and_recommendation = service.get_item_statistics_and_recommendation(
        raw_auction_items_map
    )

    return MarketChartResponse(
        item_data=statistics_and_recommendation.item_data,
        item_statistics=statistics_and_recommendation.item_statistics,
        recommendation=statistics_and_recommendation.recommendation,
    )
