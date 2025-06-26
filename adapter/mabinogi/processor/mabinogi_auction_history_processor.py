from typing import List

from adapter.mabinogi.model.AuctionHistoryDto import AuctionHistoryDto
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.processor.aggregator import AuctionHistoryGroupByHour


class MabinogiAuctionHistoryProcessor:

    def __init__(self, auction_items: List[AuctionHistoryDto]):
        self.auction_items = auction_items

    def get_auction_history_group_by_hourly(self) -> dict[str, list[AuctionItemDto]]:
        return AuctionHistoryGroupByHour(auction_items=self.auction_items) \
            .execute()
