from typing import List, Dict

from adapter.mabinogi.model.Report import Report
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto

from .sorter import Sorter


class MabinogiReportProcessor:

    def __init__(self, sorter: Sorter):
        self.auction_items = sorter.execute(direction="ASC")

    def execute(self):
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
