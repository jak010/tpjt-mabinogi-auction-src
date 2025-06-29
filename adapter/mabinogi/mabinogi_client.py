from typing import List

import requests

from .model.AuctionHistoryDto import AuctionHistoryDto
from .model.AuctionItemDto import AuctionItemDto
from .model.Item import Item
from adapter.mabinogi.processor.filter.mabinogi_auction_item_filter import filter_auction_items_by_days


class MabinogiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://open.api.nexon.com"

    def _get_headers(self) -> dict:
        return {
            "x-nxopen-api-key": self.api_key
        }

    def get_auction_items(self, item_name: str, item_category: str = None, days: int = 7) -> List[AuctionItemDto]:
        """ 경매장 매물 검색

        Docs:
            /mabinogi/v1/auction/list

        """
        suffix_url = "/mabinogi/v1/auction/list"

        params = {
            "item_name": item_name
        }
        if item_category:
            params["auction_item_category"] = item_category

        r = requests.get(
            self.base_url + suffix_url,
            headers=self._get_headers(),
            params=params
        )

        result: List[AuctionItemDto] = []
        if r.status_code == 200:
            for item_data in r.json()["auction_item"]:
                result.append(AuctionItemDto(**item_data))

            return filter_auction_items_by_days(result, days)

        raise r.raise_for_status()

    def get_auction_hsitory_items(self, item: Item) -> List[AuctionHistoryDto]:
        """ 경매장 거래내역 검색 """
        suffix_url = "/mabinogi/v1/auction/history"

        r = requests.get(
            self.base_url + suffix_url,
            headers=self._get_headers(),
            params={
                "auction_item_category": item.auction_item_category,
                "item_name": item.item_name
            }
        )
        if r.status_code == 200:
            return [AuctionHistoryDto(**item) for item in r.json()["auction_history"]]

        raise r.raise_for_status()
