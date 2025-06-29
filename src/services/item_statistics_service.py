import statistics
from typing import List, Optional
from fastapi import Depends
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository
from src.controller.schema.market_schema import ItemStatisticResponse
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto

class ItemStatisticsService:
    def __init__(
            self,
            repository: MabinogiAuctionRepository = Depends(MabinogiAuctionRepository),
    ):
        self.repository = repository

    def get_item_statistics(self, item_name: str) -> ItemStatisticResponse:
        auction_items: List[AuctionItemDto] = self.repository.get_auction_items(item_name=item_name)

        if not auction_items:
            return ItemStatisticResponse(
                item_name=item_name,
                total_items=0,
                average_price=0,
                time_based_average_price=0,
                min_price=0,
                max_price=0,
                acquisition_rate_per_30_min=0.0,
                acquisition_rate_per_hour=0.0,
                profit_per_hour=0.0,
                standard_deviation=0.0,
                trade_volume=0,
                error="No data found for this item."
            )

        total_items = len(auction_items)
        prices = [item.auction_price_per_unit for item in auction_items]
        
        average_price = sum(prices) // total_items if total_items > 0 else 0
        min_price = min(prices)
        max_price = max(prices)
        
        standard_deviation = statistics.stdev(prices) if len(prices) > 1 else 0.0
        trade_volume = sum(item.item_count for item in auction_items)

        # TODO: Implement time_based_average_price, acquisition_rate_per_30_min, acquisition_rate_per_hour, profit_per_hour
        # For now, setting them to placeholder values or simple calculations
        time_based_average_price = average_price # Placeholder
        acquisition_rate_per_30_min = 0.0 # Placeholder
        acquisition_rate_per_hour = 0.0 # Placeholder
        profit_per_hour = 0.0 # Placeholder

        return ItemStatisticResponse(
            item_name=item_name,
            total_items=total_items,
            average_price=average_price,
            time_based_average_price=time_based_average_price,
            min_price=min_price,
            max_price=max_price,
            acquisition_rate_per_30_min=acquisition_rate_per_30_min,
            acquisition_rate_per_hour=acquisition_rate_per_hour,
            profit_per_hour=profit_per_hour,
            standard_deviation=standard_deviation,
            trade_volume=trade_volume
        )
