from abc import ABCMeta
from collections import defaultdict
from typing import List, Dict

from model.AuctionHistoryDto import AuctionHistoryDto
from model.AuctionItemDto import AuctionItemDto


class AuctionItemAggregator(metaclass=ABCMeta):

    def execute(self, *args, **kwargs): ...


class AuctionItemGroupByHour(AuctionItemAggregator):
    """ acution_items을 한 시간 단위로 그룹핑 """

    def __init__(self, auction_items: List[AuctionItemDto | AuctionHistoryDto]):
        self.auction_items = auction_items

    def execute(self) -> Dict[str, List[AuctionItemDto]]:
        result = defaultdict(list)
        for auction_item in self.auction_items:
            auction_item_hour = auction_item.get_date_auction_expire_kst() \
                .replace(minute=0, second=0, microsecond=0).isoformat()
            result[auction_item_hour].append(auction_item)
        return result


class AuctionHistoryGroupByHour(AuctionItemAggregator):
    """ acution history를 한 시간 단위로 그룹 """

    def __init__(self, auction_items: List[AuctionItemDto | AuctionHistoryDto]):
        self.auction_items = auction_items

    def execute(self) -> Dict[str, List[AuctionItemDto]]:
        result = defaultdict(list)
        for auction_item in self.auction_items:
            auction_item_hour = auction_item.get_date_auction_buy_kst() \
                .replace(minute=0, second=0, microsecond=0).isoformat()
            result[auction_item_hour].append(auction_item)
        return result