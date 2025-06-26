from typing import List, Dict, Any

from fastapi import Depends  # FastAPI의 Depends를 import 합니다.

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item
from src.controller.schema.market_schema import MarketItemRequest
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository
from src.services.auction_item_aggregator import (
    # AuctionItemAggregator,
    AuctionItemDataProcessor
)


class MarketService:
    def __init__(
            self,
            repository: MabinogiAuctionRepository = Depends(MabinogiAuctionRepository),
            aggregator: AuctionItemDataProcessor = Depends(AuctionItemDataProcessor)
    ):
        self.repository = repository
        self.aggregator = aggregator

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """ 입력받은 Item 정보를 이용하여 경매장 매물 검색

        """

        market_items = self.repository.get_auction_items(
            item=Item(
                auction_item_category=request.item_category,
                item_name=request.item_name
            )
        )

        aggregated_items = self.aggregator.process_auction_data_for_chart(market_items)

        return aggregated_items

    def get_item_statistics_and_recommendation(self, items_data: Dict[str, List[AuctionItemDto]]) -> Dict[str, Any]:
        """
        여러 아이템에 대한 통계를 계산하고 추천을 생성합니다.
        items_data는 {item_name: [AuctionItemDto, ...]} 형태의 딕셔너리입니다.
        """
        all_item_stats = []

        for item_name, data in items_data.items():
            valid_prices = [
                item.auction_price_per_unit
                for item in data
                if item.auction_price_per_unit is not None
            ]

            if not valid_prices:
                all_item_stats.append(
                    {
                        "itemName": item_name,
                        "totalItems": len(data),
                        "averagePrice": 0,
                        "timeBasedAveragePrice": 0,
                        "minPrice": 0,
                        "maxPrice": 0,
                        "acquisitionRatePer30Min": 0,
                        "acquisitionRatePerHour": 0,
                        "profitPerHour": 0,
                        "error": "유효한 데이터 없음."
                    }
                )
                continue

            total_items = len(data)
            min_price = min(valid_prices)
            max_price = max(valid_prices)
            average_price = sum(valid_prices) / len(valid_prices)

            # Calculate time-based average price (average of lowest prices over time)
            # AuctionItemAggregator에서 이미 최저 가격으로 필터링된 데이터를 받으므로,
            # 여기서는 단순히 해당 데이터의 평균을 계산합니다.
            time_based_average_price = sum(valid_prices) / len(valid_prices)

            acquisition_rate_per_30_min = 0

            # Set acquisition rates based on item name (from chart.html)
            if item_name == '고급 가죽':
                acquisition_rate_per_30_min = (12 + 15) / 2  # Average of 12-15
            elif item_name == '순수의 결정':
                acquisition_rate_per_30_min = 30

            acquisition_rate_per_hour = acquisition_rate_per_30_min * 2
            profit_per_hour = time_based_average_price * acquisition_rate_per_hour

            all_item_stats.append(self._calculate_item_statistics(item_name, data))

        recommendation_text = self._generate_recommendation_text(all_item_stats)

        return {
            "itemStatistics": all_item_stats,
            "recommendation": recommendation_text
        }

    def _calculate_item_statistics(self, item_name: str, data: List[AuctionItemDto]) -> Dict[str, Any]:
        valid_prices = [item.auction_price_per_unit for item in data if item.auction_price_per_unit is not None]

        if not valid_prices:
            return self._get_empty_statistics(item_name, len(data))

        total_items = len(data)
        min_price = min(valid_prices)
        max_price = max(valid_prices)
        average_price = sum(valid_prices) / len(valid_prices)
        time_based_average_price = average_price  # 이미 필터링된 데이터이므로 동일

        acquisition_rate_per_30_min = self._get_acquisition_rate_per_30_min(item_name)
        acquisition_rate_per_hour = acquisition_rate_per_30_min * 2
        profit_per_hour = time_based_average_price * acquisition_rate_per_hour

        return {
            "itemName": item_name,
            "totalItems": total_items,
            "averagePrice": round(average_price),
            "timeBasedAveragePrice": round(time_based_average_price),
            "minPrice": min_price,
            "maxPrice": max_price,
            "acquisitionRatePer30Min": acquisition_rate_per_30_min,
            "acquisitionRatePerHour": acquisition_rate_per_hour,
            "profitPerHour": round(profit_per_hour)
        }

    def _get_empty_statistics(self, item_name: str, total_items: int) -> Dict[str, Any]:
        return {
            "itemName": item_name,
            "totalItems": total_items,
            "averagePrice": 0,
            "timeBasedAveragePrice": 0,
            "minPrice": 0,
            "maxPrice": 0,
            "acquisitionRatePer30Min": 0,
            "acquisitionRatePerHour": 0,
            "profitPerHour": 0,
            "error": "유효한 데이터 없음."
        }

    def _get_acquisition_rate_per_30_min(self, item_name: str) -> float:
        if item_name == '고급 가죽':
            return (12 + 15) / 2
        elif item_name == '순수의 결정':
            return 30
        return 0

    def _generate_recommendation_text(self, all_item_stats: List[Dict[str, Any]]) -> str:
        recommendation_text = '추천을 생성할 충분한 데이터가 없습니다.'
        profitable_items = [item for item in all_item_stats if item["profitPerHour"] > 0]

        if profitable_items:
            profitable_items.sort(key=lambda x: x["profitPerHour"], reverse=True)
            recommendation_parts = [
                f'{item["itemName"]} (시간당 예상 수익: {item["profitPerHour"]} 골드)'
                for item in profitable_items
            ]
            recommendation_text = '시간당 예상 수익을 고려할 때, 다음 아이템을 획득하는 것이 유리할 수 있습니다: ' + ', '.join(recommendation_parts)
        return recommendation_text
