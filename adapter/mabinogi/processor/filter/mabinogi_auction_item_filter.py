from datetime import datetime, timedelta
from typing import List

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
# from src.utils.time_utils import TZ_KST


def filter_auction_items_by_days(items: List[AuctionItemDto], days: int) -> List[AuctionItemDto]:
    """
    주어진 일수 내에 만료되는 경매장 아이템만 필터링합니다.
    """
    current_kst = datetime.now(TZ_KST)
    end_date = current_kst + timedelta(days=days)

    filtered_result = [
        item_dto for item_dto in items
        if item_dto.get_date_auction_expire_kst() <= end_date
    ]
    return filtered_result

def filter_auction_items_by_min_price(items: List[AuctionItemDto]) -> List[AuctionItemDto]:
    """
    최소값 위주로 매물을 정렬한다
    """
    return sorted(items, key=lambda x: x.auction_price_per_unit)


