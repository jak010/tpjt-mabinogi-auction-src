from typing import List, Dict

from mabinogi.model.Report import Report
from model.AuctionItemDto import AuctionItemDto


class MabinogiDataProcessor:

    def __init__(self, auction_items: Dict[str, List[AuctionItemDto]]):
        self.auction_items = auction_items

    def get_report(self):
        """ 시간대별, 평균가, 최저가, 최고가, 판매수량,  """

        reports = []
        for date, items in self.auction_items.items():
            item_list = [item.auction_price_per_unit for item in items]

            reports.append(
                Report(
                    dated_at=date,
                    total_unit=sum([item.item_count for item in items]),
                    max_price=max(item_list),
                    low_price=min(item_list),
                    average_price=int(sum(item_list) / len(item_list))
                )
            )

        return reports
