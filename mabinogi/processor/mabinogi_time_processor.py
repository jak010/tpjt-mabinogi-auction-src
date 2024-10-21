from typing import List

from model.AuctionHistoryDto import AuctionHistoryDto
from model.AuctionItemDto import AuctionItemDto
from processor.filter import AuctionItemFilterUntilTwoDays


class MabinogiTimeProcessor:

    def __init__(self, auction_items: List[AuctionItemDto | AuctionHistoryDto]):
        self.auction_items = auction_items

    def get_auction_item_with_two_days(self) -> List[AuctionItemDto | AuctionHistoryDto]:
        return AuctionItemFilterUntilTwoDays(auction_items=self.auction_items) \
            .execute()
