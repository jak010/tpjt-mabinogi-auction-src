from typing import List, Dict

from model.AuctionItemDto import AuctionItemDto
from .aggregator import AuctionItemGroupByHour


class MabinogiAuctionItemProcessor:

    def __init__(self, auction_items: List[AuctionItemDto]):
        self.auction_items = auction_items

    def get_auction_items_group_by_hourly(self) -> Dict[str, List[AuctionItemDto]]:
        return AuctionItemGroupByHour(auction_items=self.auction_items) \
            .execute()
