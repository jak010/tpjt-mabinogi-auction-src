from typing import List, Dict

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.controller.schema.market_schema import ItemStatisticResponse


class ItemStatisticsService:
    def process_item_data_for_statistics(
            self,
            items_data: Dict[str, List[AuctionItemDto]],
    ) -> List[ItemStatisticResponse]:
        """
        각 아이템 데이터에 대해 통계를 계산합니다.
        """
        all_item_stats = []
        for item_name, data in items_data.items():
            all_item_stats.append(self.calculate_item_statistics(item_name, data))
        return all_item_stats

    def calculate_item_statistics(
            self,
            item_name: str,
            data: List[AuctionItemDto],
    ) -> ItemStatisticResponse:
        """
        단일 아이템에 대한 통계를 계산합니다.
        """
        valid_prices = [
            item.auction_price_per_unit
            for item in data
            if item.auction_price_per_unit is not None
        ]

        if not valid_prices:
            return self.get_empty_statistics(item_name, len(data))

        total_items = len(data)
        min_price = min(valid_prices)
        max_price = max(valid_prices)
        average_price = sum(valid_prices) / len(valid_prices)
        # AuctionItemAggregator에서 이미 최저 가격으로 필터링된 데이터를 받으므로,
        # 여기서는 단순히 해당 데이터의 평균을 계산합니다.
        time_based_average_price = average_price

        acquisition_rate_per_30_min = self.get_acquisition_rate_per_30_min(item_name)
        acquisition_rate_per_hour = acquisition_rate_per_30_min * 2
        profit_per_hour = time_based_average_price * acquisition_rate_per_hour

        return ItemStatisticResponse(
            item_name=item_name,
            total_items=total_items,
            average_price=round(average_price),
            time_based_average_price=round(time_based_average_price),
            min_price=min_price,
            max_price=max_price,
            acquisition_rate_per_30_min=acquisition_rate_per_30_min,
            acquisition_rate_per_hour=acquisition_rate_per_hour,
            profit_per_hour=round(profit_per_hour),
        )

    def get_empty_statistics(
            self,
            item_name: str,
            total_items: int,
    ) -> ItemStatisticResponse:
        """
        유효한 데이터가 없을 경우 빈 통계 딕셔너리를 반환합니다.
        """
        return ItemStatisticResponse(
            item_name=item_name,
            total_items=total_items,
            average_price=0,
            time_based_average_price=0,
            min_price=0,
            max_price=0,
            acquisition_rate_per_30_min=0,
            acquisition_rate_per_hour=0,
            profit_per_hour=0,
            error="유효한 데이터 없음.",
        )

    def get_acquisition_rate_per_30_min(self, item_name: str) -> float:
        """
        아이템 이름에 따른 30분당 획득률을 반환합니다.
        """
        if item_name == '고급 가죽':
            return (12 + 15) / 2
        elif item_name == '순수의 결정':
            return 30
        return 0
