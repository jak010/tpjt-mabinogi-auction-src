from typing import List

from fastapi import Depends

from typing import List

from fastapi import Depends

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item
from src.controller.schema.market_schema import (
    MarketItemRequest
)
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository
from src.services.interfaces import IMarketService


class MarketService(IMarketService):
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
        입력받은 Item 정보를 이용하여 마비노기 경매장에서 매물을 검색하고 집계합니다.
        """
        items = self.repository.get_auction_items(item_name=request.item_name)
        return items
