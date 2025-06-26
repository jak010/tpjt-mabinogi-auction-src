from datetime import datetime
from abc import ABCMeta
from typing import List, Dict, Union

from adapter.mabinogi.model.AuctionHistoryDto import AuctionHistoryDto
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto

from utils import time_utils


class Filter(metaclass=ABCMeta):

    def __init__(self, auction_items):
        self.auction_items: List[AuctionItemDto | AuctionHistoryDto] = auction_items

    def execute(self, *args, **kwrags): ...


class AuctionItemFilterUntilTwoDays(Filter):

    def execute(self) -> List[AuctionItemDto | AuctionHistoryDto]:

        result = []
        for auction_item in self.auction_items:
            if time_utils.current_kst < auction_item.get_date_auction_expire_kst() < time_utils.get_day_after_two_days():
                result.append(auction_item)
        return result


class AutionItemFilterGroupByMinutes(Filter):

    def execute(self) -> Dict[datetime, List[AuctionItemDto | AuctionHistoryDto]]:

        result = {}

        for auction_item in self.auction_items:
            expired_date = auction_item.get_date_auction_expire_kst()

            _parsed_expired_date = expired_date.strftime("%Y:%m:%d %H:%M")
            if _parsed_expired_date not in result:
                result[_parsed_expired_date] = [auction_item]
            else:
                result[_parsed_expired_date].append(auction_item)

        return result
