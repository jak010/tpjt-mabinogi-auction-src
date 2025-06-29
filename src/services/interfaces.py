from abc import ABCMeta
from typing import List

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.controller.schema.market_schema import MarketItemRequest


class IMarketService(metaclass=ABCMeta):
    """
    마비노기 경매장 데이터 조회 및 통계, 추천 기능을 제공하는 서비스.
    """

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """ 입력받은 Item 정보로 마비노기 경매장에서 매물을 검색해서 반환합니다."""
        ...
