from typing import List

import requests

from .model.AuctionHistoryDto import AuctionHistoryDto
from .model.AuctionItemDto import AuctionItemDto
from .model.Item import Item


class MabinogiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://open.api.nexon.com"

    def _get_headers(self) -> dict:
        return {
            "x-nxopen-api-key": self.api_key
        }

    def get_auction_items(self, item: Item) -> List[AuctionItemDto]:
        """ 경매장 매물 검색 """
        suffix_url = "/mabinogi/v1/auction/list"

        r = requests.get(
            self.base_url + suffix_url,
            headers=self._get_headers(),
            params={
                "auction_item_category": item.auction_item_category,
                "item_name": item.item_name
            }
        )
        if r.status_code == 200:
            return [AuctionItemDto(**item) for item in r.json()["auction_item"]]

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
