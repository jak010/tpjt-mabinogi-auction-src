from typing import List, Dict, Any

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item

import os
from dotenv import load_dotenv
from collections import defaultdict

from src.controller.markets import MarketItemRequest
from src.services.auction_item_aggregator import AuctionItemAggregator

load_dotenv()


class MarketService:
    client: MabinogiClient = MabinogiClient(api_key=os.environ['MABINOGI_API_KEY'])
    aggregator: AuctionItemAggregator = AuctionItemAggregator()

    def get_market_items(self, request: MarketItemRequest) -> List[AuctionItemDto]:
        """ 입력받은 Item 정보를 이용하여 경매장 매물 검색

        """

        market_items = self.client.get_auction_items(
            item=Item(
                auction_item_category=request.item_category,
                item_name=request.item_name
            )
        )

        aggregated_items = self.aggregator.aggregate_market_items_by_time(market_items)
        # aggregated_items는 이미 _process_lowest_price_data에서 정렬되어 반환됩니다.

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
                all_item_stats.append({
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
                })
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

            all_item_stats.append({
                "itemName": item_name,
                "totalItems": total_items,
                "averagePrice": round(average_price),
                "timeBasedAveragePrice": round(time_based_average_price),
                "minPrice": min_price,
                "maxPrice": max_price,
                "acquisitionRatePer30Min": acquisition_rate_per_30_min,
                "acquisitionRatePerHour": acquisition_rate_per_hour,
                "profitPerHour": round(profit_per_hour)
            })

        # Recommendation logic
        recommendation_text = '추천을 생성할 충분한 데이터가 없습니다.'
        profitable_items = [item for item in all_item_stats if item["profitPerHour"] > 0]

        if profitable_items:
            profitable_items.sort(key=lambda x: x["profitPerHour"], reverse=True)
            recommendation_parts = []
            for item in profitable_items:
                recommendation_parts.append(
                    f'{item["itemName"]} (시간당 예상 수익: {item["profitPerHour"]} 골드)'
                )
            recommendation_text = '시간당 예상 수익을 고려할 때, 다음 아이템을 획득하는 것이 유리할 수 있습니다: ' + ', '.join(recommendation_parts)
        
        return {
            "itemStatistics": all_item_stats,
            "recommendation": recommendation_text
        }
