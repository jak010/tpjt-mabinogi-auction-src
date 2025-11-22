from __future__ import annotations

import random
from typing import List

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from bot.dto.money_item import MoneyItem
from bot.revenue.calculate_revenue import calculate_hourly_revenue


class RecommendService:

    def __init__(self,
                 recommend_items: List[MoneyItem],
                 mabinogi_client: MabinogiClient
                 ):
        self.recommend_item: MoneyItem = random.choices(recommend_items, k=1)[0]
        self.mabinogi_client = mabinogi_client

    def _get_auction_list_top5(self) -> List[AuctionItemDto]:
        auction_items: List[AuctionItemDto] = self.mabinogi_client.get_auction_items(
            item_category=self.recommend_item.category,
            item_name=self.recommend_item.name
        )
        return auction_items[0:5]

    def get_summary_with_items(self, recommend_item: MoneyItem, recommend_items: List[AuctionItemDto]):
        avg_price = sum([e.auction_price_per_unit for e in recommend_items]) / len(recommend_items)
        total_count = sum([e.item_count for e in recommend_items])

        return self._outbox(
            item_name=recommend_item.name,
            item_per_minute=recommend_item.time_per_minute,
            item_per_count=recommend_item.time_per_count,
            avg_price=avg_price,
            total_count=total_count,
            expect=calculate_hourly_revenue(avg_price, recommend_item.time_per_minute, recommend_item.time_per_count)
        )

    def get_summary(self):
        aution_items = self._get_auction_list_top5()

        avg_price = sum([e.auction_price_per_unit for e in aution_items]) / len(aution_items)
        total_count = sum([e.item_count for e in aution_items])

        return self._outbox(
            item_name=self.recommend_item.name,
            item_per_minute=self.recommend_item.time_per_minute,
            item_per_count=self.recommend_item.time_per_count,
            avg_price=avg_price,
            total_count=total_count,
            expect=calculate_hourly_revenue(avg_price, self.recommend_item.time_per_minute,
                                            self.recommend_item.time_per_count)
        )

    def _outbox(self, item_name, item_per_minute, item_per_count, avg_price, total_count, expect):
        return "[검쨩봇의 추천노기]\n" \
               f"아이템: {item_name}\n" \
               f"단위(분): {item_per_minute} / 기대 획득 수: {item_per_count} \n" \
               f"경매장 최저가 평균 가격: {avg_price} / 매물: {total_count}\n" \
               f"1시간 기대 수익률: {expect}\n"
