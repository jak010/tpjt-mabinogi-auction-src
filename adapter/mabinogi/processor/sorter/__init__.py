from abc import ABCMeta
from typing import List, Literal, Dict

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


class Sorter(metaclass=ABCMeta):

    def execute(self, direction: Literal["DESC"] | Literal["ASC"]): ...


class MabinogiAuctionItemSorter(Sorter):

    def __init__(self, auction_items: Dict[str, List[AuctionItemDto]]):
        self.auction_items = auction_items

    def execute(self, direction: Literal["DESC"] | Literal["ASC"]) -> Dict[str, List[AuctionItemDto]]:
        if direction == "ASC":
            return {k: v for k, v in sorted(self.auction_items.items(), key=lambda x: x, reverse=True)}
        if direction == "DESC":
            return {k: v for k, v in sorted(self.auction_items.items(), key=lambda x: x)}

        raise Exception("Not Support Opperator")
