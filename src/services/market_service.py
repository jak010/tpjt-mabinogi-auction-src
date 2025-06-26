from datetime import datetime
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
    """
    마비노기 경매장 데이터 조회 및 통계, 추천 기능을 제공하는 서비스입니다.
    """

    def __init__(
            self,
            repository: MabinogiAuctionRepository = Depends(MabinogiAuctionRepository),
            aggregator: AuctionItemDataProcessor = Depends(AuctionItemDataProcessor),
            item_statistics_service: ItemStatisticsService = Depends(ItemStatisticsService),
            recommendation_service: RecommendationService = Depends(RecommendationService),
    ):
        """
        MarketService의 새 인스턴스를 초기화합니다.

        Args:
            repository (MabinogiAuctionRepository): 경매장 데이터 접근을 위한 레포지토리.
            aggregator (AuctionItemDataProcessor): 경매 아이템 데이터 처리를 위한 프로세서.
            item_statistics_service (ItemStatisticsService): 아이템 통계 계산을 위한 서비스.
            recommendation_service (RecommendationService): 추천 텍스트 생성을 위한 서비스.
        """
        self.repository = repository
        self.aggregator = aggregator
        self.item_statistics_service = item_statistics_service
        self.recommendation_service = recommendation_service

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """
        입력받은 Item 정보를 이용하여 경매장 매물을 검색하고 집계합니다.

        Args:
            request (MarketItemRequest): 검색할 아이템의 카테고리와 이름을 포함하는 요청 객체.

        Returns:
            List[AuctionItemDto]: 집계된 경매 아이템 데이터 리스트.
        """
        market_items = self.repository.get_auction_items(
            item=Item(
                auction_item_category=request.item_category,
                item_name=request.item_name,
            )
        )

        aggregated_items = self.aggregator.process_auction_data_for_chart(market_items)

        # expired 시간이 얼마 안남은 순서로 정렬
        # date_auction_expire 필드를 사용하여 정렬
        aggregated_items.sort(key=lambda item: item.get_date_auction_expire_kst())

        return aggregated_items

    def get_item_statistics_and_recommendation(
            self,
            items_data: Dict[str, List[AuctionItemDto]],
    ) -> MarketChartResponse:
        """
        여러 아이템에 대한 통계를 계산하고 추천을 생성합니다.

        Args:
            items_data (Dict[str, List[AuctionItemDto]]): 아이템 이름별 경매 아이템 데이터 딕셔너리.
                                                          예: {'아이템명': [AuctionItemDto, ...]}

        Returns:
            MarketChartResponse: 아이템 데이터, 통계, 추천 텍스트를 포함하는 응답 객체.
        """
        all_item_stats = self.item_statistics_service.process_item_data_for_statistics(items_data)
        recommendation_text = self.recommendation_service.generate_recommendation_text(all_item_stats)

        converted_item_data = items_data

        return MarketChartResponse(
            item_data=converted_item_data,
            item_statistics=all_item_stats,
            recommendation=recommendation_text,
        )
