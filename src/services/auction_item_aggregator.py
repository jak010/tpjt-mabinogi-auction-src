from collections import defaultdict
from typing import List
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from datetime import datetime, timezone, timedelta


class AuctionItemAggregator:
    """
    경매장 아이템 데이터를 시간별로 집계하고 처리하는 클래스입니다.
    동일한 시간에 만료되는 아이템들의 가격을 평균내고 수량을 합산합니다.
    """

    def aggregate_market_items_by_time(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        경매장 아이템들을 만료 시간을 기준으로 그룹화하고, 가격을 평균내며 수량을 합산합니다.
        """
        # 1. 유효성 검사 및 이상치 제거, 시간 필터링
        filtered_items = self._filter_and_clean_items(market_items)

        # 2. 동일한 시간에 만료되는 아이템 중 최저 가격 선택
        lowest_price_items = self._get_lowest_price_per_timestamp(filtered_items)

        # 3. 집계 (기존 로직 유지, 단일 아이템이므로 평균 대신 해당 아이템 값 사용)
        aggregated_results = self._process_lowest_price_data(lowest_price_items)
        return aggregated_results

    def _filter_and_clean_items(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        유효하지 않은 가격 데이터를 필터링하고, 이상치를 제거하며, 특정 시간 이후 데이터를 제외합니다.
        """
        cleaned_items = []
        
        # 현재 KST 날짜의 자정 (00:00:00)을 기준으로 1.5일 후의 타임스탬프 계산
        now_kst = datetime.now(timezone.utc) + timedelta(hours=9) # KST는 UTC+9
        kst_midnight = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
        kst_plus_one_point_five_days = kst_midnight + timedelta(days=1.5)

        # 평균 가격 계산 (이상치 필터링을 위해)
        valid_prices = [
            item.auction_price_per_unit
            for item in market_items
            if item.auction_price_per_unit is not None
        ]
        average_price = sum(valid_prices) / len(valid_prices) if valid_prices else 0
        outlier_threshold = average_price * 2 if average_price > 0 else float('inf') # 평균이 0이면 이상치 필터링 안함

        for item in market_items:
            # auction_price_per_unit이 None이 아니고, 이상치가 아니며, 1.5일 이후 데이터가 아닌 경우
            if (
                item.auction_price_per_unit is not None and
                (average_price == 0 or item.auction_price_per_unit <= outlier_threshold) and
                item.get_date_auction_expire_kst() < kst_plus_one_point_five_days
            ):
                cleaned_items.append(item)
        return cleaned_items

    def _get_lowest_price_per_timestamp(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        동일한 만료 시간을 가진 아이템들 중에서 최저 가격 아이템만 선택합니다.
        """
        lowest_price_map = {} # {timestamp: AuctionItemDto}
        for item in market_items:
            timestamp = item.get_date_auction_expire_kst()
            if timestamp not in lowest_price_map or item.auction_price_per_unit < lowest_price_map[timestamp].auction_price_per_unit:
                lowest_price_map[timestamp] = item
        return list(lowest_price_map.values())

    def _process_lowest_price_data(self, lowest_price_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        최저 가격 아이템 리스트를 받아 집계된 AuctionItemDto 객체 리스트를 생성합니다.
        이 경우, 이미 최저 가격이 선택되었으므로 추가적인 평균 계산은 필요 없습니다.
        """
        # 단순히 정렬만 수행
        return sorted(lowest_price_items, key=lambda x: x.get_date_auction_expire_kst())
