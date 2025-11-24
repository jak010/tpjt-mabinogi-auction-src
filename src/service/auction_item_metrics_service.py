from __future__ import annotations

from typing import List

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


class AuctionItemsMetricsService:
    def __init__(self, aution_items: List[AuctionItemDto]):
        self.auction_items = aution_items

    def size(self):
        return len(self.auction_items)

    def total_price_per_unit(self):
        return sum([e.auction_price_per_unit for e in self.auction_items])

    def average(self):
        try:
            return self.total_price_per_unit() / self.size()
        except ZeroDivisionError:
            return 0

    def calculate_hourly_revenue(self, time_per_minute: int, timr_per_count: int) -> str:
        """ 주어진 아이템 기준으로 시간당 매출을 계산 """
        intervals_per_hour = 60 / time_per_minute  # 1시간 동안 반복되는 횟수
        items_per_hour = intervals_per_hour * timr_per_count
        hourly_revenue = items_per_hour * self.average()
        return f"{int(hourly_revenue):,}"  # 3자리마다 쉼표 추가
