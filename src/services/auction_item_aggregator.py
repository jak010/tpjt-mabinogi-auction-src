from collections import defaultdict
from typing import List
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from datetime import datetime, timezone


class AuctionItemAggregator:
    """
    경매장 아이템 데이터를 시간별로 집계하고 처리하는 클래스입니다.
    동일한 시간에 만료되는 아이템들의 가격을 평균내고 수량을 합산합니다.
    """

    def aggregate_market_items_by_time(self, market_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """
        경매장 아이템들을 만료 시간을 기준으로 그룹화하고, 가격을 평균내며 수량을 합산합니다.
        """
        grouped_items = self._group_items_by_time(market_items)
        aggregated_results = self._process_grouped_data(grouped_items)
        return aggregated_results

    def _group_items_by_time(self, market_items: List[AuctionItemDto]):
        """
        경매장 아이템들을 KST 만료 시간을 기준으로 그룹화하는 헬퍼 메서드입니다.
        """
        grouped_items = defaultdict(lambda: {'total_price': 0, 'total_count': 0, 'item_count_sum': 0, 'items': []})
        for item in market_items:
            group_key = item.get_date_auction_expire_kst()
            grouped_items[group_key]['total_price'] += item.auction_price_per_unit * item.item_count
            grouped_items[group_key]['total_count'] += item.item_count
            grouped_items[group_key]['item_count_sum'] += item.item_count
            grouped_items[group_key]['items'].append(item)
        return grouped_items

    def _process_grouped_data(self, grouped_items: defaultdict) -> List[AuctionItemDto]:
        """
        그룹화된 경매장 아이템 데이터를 처리하고 집계된 AuctionItemDto 객체를 생성하는 헬퍼 메서드입니다.
        """
        aggregated_results = []
        for group_key, data in grouped_items.items():
            aggregated_item = self._create_aggregated_auction_item(group_key, data)
            aggregated_results.append(aggregated_item)
        return aggregated_results

    def _create_aggregated_auction_item(self, group_key: datetime, data: dict) -> AuctionItemDto:
        """
        단일 집계된 AuctionItemDto를 생성하는 헬퍼 메서드입니다.
        """
        average_price_per_unit = round(data['total_price'] / data['total_count']) if data['total_count'] > 0 else 0
        template_item = data['items'][0]  # 그룹 내 일관성을 가정합니다.

        return AuctionItemDto(
            item_name=template_item.item_name,
            item_display_name=template_item.item_display_name,
            item_count=data['item_count_sum'],
            auction_price_per_unit=average_price_per_unit,
            date_auction_expire=group_key.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            auction_item_category=template_item.auction_item_category,
            item_option=template_item.item_option
        )
