from datetime import datetime
from typing import List, Dict

from adapter.mabinogi.model.AuctionHistoryDto import AuctionHistoryDto
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.processor.filter import AuctionItemFilterUntilTwoDays, AutionItemFilterGroupByMinutes


class MabinogiTimeProcessor:

    def __init__(self, auction_items: List[AuctionItemDto | AuctionHistoryDto]):
        self.auction_items = auction_items

    def get_auction_item_until_two_days(self) -> List[AuctionItemDto | AuctionHistoryDto]:
        return AuctionItemFilterUntilTwoDays(auction_items=self.auction_items) \
            .execute()

    def get_auction_item_group_by_minutes(self) -> Dict[datetime, List[AuctionItemDto | AuctionHistoryDto]]:
        return AutionItemFilterGroupByMinutes(auction_items=self.auction_items) \
            .execute()
