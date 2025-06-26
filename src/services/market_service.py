from typing import List

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item

import os
from dotenv import load_dotenv

from src.controller.markets import MarketItemRequest
from src.services.auction_item_aggregator import AuctionItemAggregator

load_dotenv()


class MarketService:
    client: MabinogiClient = MabinogiClient(api_key=os.environ['MABINOGI_API_KEY'])
    aggregator: AuctionItemAggregator = AuctionItemAggregator()

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """ 입력받은 Item 정보를 이용하여 경매장 매물 검색

        """

        market_items = self.client.get_auction_items(
            item=Item(
                auction_item_category=request.item_category,
                item_name=request.item_name
            )
        )

        aggregated_items = self.aggregator.aggregate_market_items_by_time(market_items)
        aggregated_items.sort(key=lambda x: x.get_date_auction_expire_kst())

        return aggregated_items
