from typing import List, Dict

from fastapi import Depends

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item
from src.controller.schema.market_schema import (
    MarketItemRequest,
    MarketChartResponse,
    MarketItemResponse
)
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository
from src.services.auction_item_aggregator import AuctionItemDataProcessor
from src.services.item_statistics_service import ItemStatisticsService
from src.services.recommendation_service import RecommendationService


class MarketService:
    def __init__(
            self,
            repository: MabinogiAuctionRepository = Depends(MabinogiAuctionRepository),
            aggregator: AuctionItemDataProcessor = Depends(AuctionItemDataProcessor),
            item_statistics_service: ItemStatisticsService = Depends(ItemStatisticsService),
            recommendation_service: RecommendationService = Depends(RecommendationService),
    ):
        self.repository = repository
        self.aggregator = aggregator
        self.item_statistics_service = item_statistics_service
        self.recommendation_service = recommendation_service

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """ 입력받은 Item 정보를 이용하여 경매장 매물 검색

        """

        market_items = self.repository.get_auction_items(
            item=Item(
                auction_item_category=request.item_category,
                item_name=request.item_name,
            )
        )

        aggregated_items = self.aggregator.process_auction_data_for_chart(market_items)

        return aggregated_items

    def get_item_statistics_and_recommendation(
            self,
            items_data: Dict[str, List[AuctionItemDto]],
    ) -> MarketChartResponse:
        """
        여러 아이템에 대한 통계를 계산하고 추천을 생성합니다.
        items_data는 {item_name: [AuctionItemDto, ...]} 형태의 딕셔너리입니다.
        """
        all_item_stats = self.item_statistics_service._process_item_data_for_statistics(items_data)
        recommendation_text = self.recommendation_service.generate_recommendation_text(all_item_stats)

        converted_item_data = {
            item_name: MarketItemResponse.with_items(data)
            for item_name, data in items_data.items()
        }

        return MarketChartResponse(
            item_data=converted_item_data,
            item_statistics=all_item_stats,
            recommendation=recommendation_text,
        )
