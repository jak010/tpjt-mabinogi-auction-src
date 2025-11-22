from __future__ import annotations

import random
from typing import List

from bot.revenue.calculate_revenue import calculate_hourly_revenue
from src.entity.item import MoneyItem
from src.entity.location import Location
from src.repository.location_repository import LocationRepository
from src.repository.item_repository import ItemRepository
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


class RecommandService:

    def __init__(self, location_repo, item_repo, mabinogi_client):
        self.location_repo: LocationRepository = location_repo
        self.item_repo: ItemRepository = item_repo
        self.mabinogi_client = mabinogi_client

    def get_random_location(self) -> Location:
        return random.sample(self.location_repo.get_all_locations(), k=1)[0]

    def fetch_by(self, item: MoneyItem) -> List[AuctionItemDto]:
        """ 마비노기 클라이언트에 입력 아이템으로 경매장 검색 """
        auction_items: List[AuctionItemDto] = self.mabinogi_client.get_auction_items(
            item_category=item.category,
            item_name=item.name
        )
        return auction_items[0:5]

    def get_summary_with_items(self,
                               location,
                               money_items: MoneyItem,
                               aution_items: List[AuctionItemDto]):

        try:
            avg_price = sum([e.auction_price_per_unit for e in aution_items]) / len(aution_items)
            total_count = sum([e.item_count for e in aution_items])
        except ZeroDivisionError:
            avg_price = 0
            total_count = 0

        return self._outbox(
            location=location,
            item_name=money_items.name,
            item_per_minute=money_items.time_per_minute,
            item_per_count=money_items.time_per_count,
            avg_price=avg_price,
            total_count=total_count,
            expect=calculate_hourly_revenue(avg_price, money_items.time_per_minute, money_items.time_per_count)
        )

    def execute(self) -> List:
        pick_location = self.get_random_location()

        money_items = self.item_repo.get_item_by_locatin_id(location_id=pick_location.location_id)

        results = []
        for money_item in money_items:
            result = self.get_summary_with_items(
                location=pick_location.name,
                money_items=money_item,
                aution_items=self.fetch_by(money_item)
            )
            results.append(result)

        return results

    def _outbox(self,location, item_name, item_per_minute, item_per_count, avg_price, total_count, expect):
        return "[검쨩봇의 추천노기]\n" \
               f"위치: {location}\n" \
               f"아이템: {item_name}\n" \
               f"단위(분): {item_per_minute} / 기대 획득 수: {item_per_count} \n" \
               f"경매장 최저가 평균 가격: {avg_price} / 매물: {total_count}\n" \
               f"1시간 기대 수익률: {expect}\n"
