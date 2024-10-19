from typing import List

import requests

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
        suffix_url = "/mabinogi/v1/auction/list"  # 경매장 매물검색

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
