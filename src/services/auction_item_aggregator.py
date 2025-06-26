from collections import defaultdict
from typing import List
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from datetime import datetime, timezone, timedelta

# 상수 정의
KST_OFFSET_HOURS = 9
DATA_VALID_DAYS_LIMIT = 2
OUTLIER_MULTIPLIER = 2


class AuctionItemDataProcessor:
    """
    경매장 아이템 데이터를 처리하고 정제하는 클래스입니다.
    주어진 아이템 목록에서 유효한 데이터를 필터링하고,
    동일한 만료 시간 내 최저 가격 아이템을 추출하며,
    최종적으로 만료 시간 기준으로 정렬된 데이터를 반환합니다.
    """

    def process_auction_data_for_chart(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        차트 표시를 위해 경매장 아이템 데이터를 처리합니다.
        유효성 검사, 이상치 제거, 최저 가격 추출 및 만료 시간 기준으로 정렬을 수행합니다.
        """
        # 1. 유효성 검사 및 이상치 제거, 시간 필터링
        filtered_items = self._filter_and_clean_auction_items(market_items)

        # 2. 동일한 시간에 만료되는 아이템 중 최저 가격 선택
        lowest_price_items = self._get_lowest_price_per_timestamp(filtered_items)

        # 3. 만료 시간 기준으로 정렬
        sorted_items = self._sort_by_expiration_time(lowest_price_items)
        return sorted_items

    def _filter_and_clean_auction_items(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        경매장 아이템 목록에서 유효하지 않은 가격 데이터를 필터링하고, 이상치를 제거하며,
        특정 시간 이후 데이터를 제외하여 정제된 리스트를 반환합니다.
        """
        cleaned_items = []

        # 현재 KST 날짜의 자정 (00:00:00)을 기준으로 1.5일 후의 타임스탬프 계산
        now_kst = datetime.now(timezone.utc) + timedelta(hours=KST_OFFSET_HOURS)
        kst_midnight = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
        data_expiration_limit = kst_midnight + timedelta(days=DATA_VALID_DAYS_LIMIT)

        valid_prices = [
            item.auction_price_per_unit
            for item in market_items
            if item.auction_price_per_unit is not None
        ]

        average_price = self._calculate_average_price(valid_prices)
        outlier_threshold = self._calculate_outlier_threshold(average_price)

        for item in market_items:
            if self._is_valid_item(item, outlier_threshold, data_expiration_limit):
                cleaned_items.append(item)
        return cleaned_items

    def _calculate_average_price(self, prices: List[int]) -> float:
        """유효한 가격 리스트의 평균을 계산합니다."""
        return sum(prices) / len(prices) if prices else 0

    def _calculate_outlier_threshold(self, average_price: float) -> float:
        """이상치 필터링을 위한 임계값을 계산합니다."""
        return average_price * OUTLIER_MULTIPLIER if average_price > 0 else float('inf')

    def _is_valid_item(self, item: AuctionItemDto, outlier_threshold: float, data_expiration_limit: datetime) -> bool:
        """아이템이 유효성 조건을 만족하는지 확인합니다."""
        return (
                item.auction_price_per_unit is not None and
                item.auction_price_per_unit <= outlier_threshold and
                item.get_date_auction_expire_kst() < data_expiration_limit
        )

    def _get_lowest_price_per_timestamp(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        동일한 만료 시간을 가진 아이템들 중에서 최저 가격 아이템만 선택합니다.
        """
        lowest_price_map = {}  # {timestamp: AuctionItemDto}
        for item in market_items:
            timestamp = item.get_date_auction_expire_kst()
            if timestamp not in lowest_price_map or item.auction_price_per_unit < lowest_price_map[timestamp].auction_price_per_unit:
                lowest_price_map[timestamp] = item
        return list(lowest_price_map.values())

    def _sort_by_expiration_time(self, items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        아이템 리스트를 만료 시간을 기준으로 정렬합니다.
        """
        return sorted(items, key=lambda x: x.get_date_auction_expire_kst())
