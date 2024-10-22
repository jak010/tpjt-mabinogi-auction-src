from abc import ABCMeta
from typing import List

from mabinogi.model.AuctionHistoryDto import AuctionHistoryDto
from mabinogi.model.AuctionItemDto import AuctionItemDto

from utils import time_utils


class Filter(metaclass=ABCMeta):

    def execute(self, *args, **kwrags): ...


class AuctionItemFilterUntilTwoDays(Filter):

    def __init__(self, auction_items):
        self.auction_items: List[AuctionItemDto | AuctionHistoryDto] = auction_items

    def execute(self) -> List[AuctionItemDto | AuctionHistoryDto]:

        result = []
        for auction_item in self.auction_items:
            if time_utils.current_kst < auction_item.get_date_auction_expire_kst() < time_utils.get_day_after_two_days():
                result.append(auction_item)
        return result
