from typing import List

from fastapi import Depends

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item
from src.controller.schema.market_schema import (
    MarketItemRequest
)
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository


class MarketService:
    """
    마비노기 경매장 데이터 조회 및 통계, 추천 기능을 제공하는 서비스입니다.
    """

    def __init__(
            self,
            repository: MabinogiAuctionRepository = Depends(MabinogiAuctionRepository),

    ):
        """
        MarketService의 새 인스턴스를 초기화합니다.

        """
        self.repository = repository

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

        return market_items
