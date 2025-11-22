from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


def calculate_hourly_revenue(avg_price_per_unit, time_per_minute: int, count_per_interval: int) -> str:
    """
    주어진 아이템 기준으로 시간당 매출을 계산
    :param item: AuctionItemDto 객체
    :param time_per_minute: 몇 분마다 획득하는지
    :param count_per_interval: time_per_minute마다 획득 수
    :return: 시간당 매출(원)
    """
    intervals_per_hour = 60 / time_per_minute            # 1시간 동안 반복되는 횟수
    items_per_hour = intervals_per_hour * count_per_interval
    hourly_revenue = items_per_hour * avg_price_per_unit
    return f"{int(hourly_revenue):,}"  # 3자리마다 쉼표 추가

