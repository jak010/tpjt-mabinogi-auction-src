from datetime import datetime
from typing import List, Dict

from model.AuctionHistoryDto import AuctionHistoryDto
from model.AuctionItemDto import AuctionItemDto
from processor.filter import AuctionItemFilterUntilTwoDays, AutionItemFilterGroupByMinutes


class MabinogiPriceExtractor:

    def __init__(self, market_data: Dict[datetime, List[AuctionItemDto | AuctionHistoryDto]]):
        self.market_data = market_data

    def get_price(self):
        """

        최저가, 평균가, 중간가, 고가, 시세변동폭, 물품갯수 추가하기

        """

        result = {}

        for date, items in self.market_data.items():
            prices = {
                "low": min([item.auction_price_per_unit for item in items]),
                "avg": sum([item.auction_price_per_unit for item in items]) / len(items),
                "high": max([item.auction_price_per_unit for item in items])
            }
            result[date] = prices

        return sorted(result.items(), key=lambda x: x[0])
