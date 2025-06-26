from typing import List, Dict, Optional

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.controller.schema.market_schema import ItemStatisticResponse


class ItemStatisticsService:
    """
    아이템 경매 데이터를 기반으로 통계를 계산하는 서비스입니다.
    """

    # 아이템별 30분당 획득률 (임시 데이터)
    _DEFAULT_ACQUISITION_RATES = {
        '고급 가죽': (12 + 15) / 2,
        '순수의 결정': 30.0,
    }

    def __init__(self, acquisition_rates: Optional[Dict[str, float]] = None):
        """
        ItemStatisticsService의 새 인스턴스를 초기화합니다.

        Args:
            acquisition_rates (Optional[Dict[str, float]]): 아이템별 30분당 획득률 맵.
                                                            제공되지 않으면 기본 획득률을 사용합니다.
        """
        self.acquisition_rates = acquisition_rates if acquisition_rates is not None else self._DEFAULT_ACQUISITION_RATES

    def process_item_data_for_statistics(
            self,
            items_by_name: Dict[str, List[AuctionItemDto]],
    ) -> List[ItemStatisticResponse]:
        """
        각 아이템 데이터에 대해 통계를 계산합니다.

        Args:
            items_by_name (Dict[str, List[AuctionItemDto]]): 아이템 이름별 경매 아이템 데이터 딕셔너리.

        Returns:
            List[ItemStatisticResponse]: 각 아이템에 대한 통계 응답 객체 리스트.
        """
        all_item_stats = []
        for item_name, auction_items in items_by_name.items():
            all_item_stats.append(self.calculate_item_statistics(item_name, auction_items))
        return all_item_stats

    def calculate_item_statistics(
            self,
            item_name: str,
            auction_items: List[AuctionItemDto],
    ) -> ItemStatisticResponse:
        """
        단일 아이템에 대한 통계를 계산합니다.

        Args:
            item_name (str): 아이템 이름.
            auction_items (List[AuctionItemDto]): 해당 아이템의 경매 데이터 리스트.

        Returns:
            ItemStatisticResponse: 단일 아이템에 대한 통계 응답 객체.
        """
        valid_prices = self._extract_valid_prices(auction_items)

        if not valid_prices:
            return self._get_empty_statistics(item_name, len(auction_items))

        total_items = len(auction_items)
        min_price = min(valid_prices)
        max_price = max(valid_prices)
        average_price = sum(valid_prices) / len(valid_prices)
        # AuctionItemAggregator에서 이미 최저 가격으로 필터링된 데이터를 받으므로,
        # 여기서는 단순히 해당 데이터의 평균을 계산합니다.
        time_based_average_price = average_price

        acquisition_rate_per_30_min = self.acquisition_rates.get(item_name, 0.0)
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

    def _extract_valid_prices(self, auction_items: List[AuctionItemDto]) -> List[int]:
        """
        경매 아이템 리스트에서 유효한 가격(None이 아닌)을 추출합니다.

        Args:
            auction_items (List[AuctionItemDto]): 경매 아이템 데이터 리스트.

        Returns:
            List[int]: 유효한 가격 리스트.
        """
        return [
            item.auction_price_per_unit
            for item in auction_items
            if item.auction_price_per_unit is not None
        ]

    def _get_empty_statistics(
            self,
            item_name: str,
            total_items: int,
    ) -> ItemStatisticResponse:
        """
        유효한 데이터가 없을 경우 빈 통계 응답 객체를 반환합니다.

        Args:
            item_name (str): 아이템 이름.
            total_items (int): 처리된 총 아이템 수 (유효한 가격이 없는 경우에도).

        Returns:
            ItemStatisticResponse: 빈 통계 응답 객체.
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
