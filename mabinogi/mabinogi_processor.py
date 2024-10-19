import operator
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

from mabinogi.model.AuctionItemDto import AuctionItemDto
from utils import time_utils


class MabinogiProcessor:

    def get_active_auctions(self, data: List[AuctionItemDto]):
        """ 현재 시간이후로 형성되어있는 매물 가져오기 """
        result = []
        for item in data["auction_item"]:
            date_auction_expire_utc = datetime.strptime(item['date_auction_expire'], '%Y-%m-%dT%H:%M:%S.%fZ')
            date_auction_expire_kst = date_auction_expire_utc.astimezone(time_utils.TZ_KST)

            if time_utils.current_kst < date_auction_expire_kst:
                result.append(item)

        return result

    def get_auction_item_in_today(self, auction_items: List[AuctionItemDto]) -> List[AuctionItemDto]:
        """ 만료시간이 '오늘'인 매물 """
        result = []
        for auction_item in auction_items:
            if time_utils.current_kst < auction_item.get_date_auction_expire_kst() < time_utils.today_midnigit():
                result.append(auction_item)
        return result

    def get_auction_items_group_by_hourly(self, auction_items: List[AuctionItemDto]) -> Dict[str, List[AuctionItemDto]]:
        """ acution_items을 한 시간 단위로 그룹 """

        result = defaultdict(list)
        for auction_item in auction_items:
            auction_item_hour = auction_item.get_date_auction_expire_kst() \
                .replace(minute=0, second=0, microsecond=0).isoformat()
            result[auction_item_hour].append(auction_item)

        return result

    def get_report(self, auction_items: Dict[str, List[AuctionItemDto]]):
        """ 시간대별, 평균가, 최저가, 최고가, 판매수량,  """
        from .model.Report import Report

        reports = []
        for date, items in auction_items.items():
            item_list = [item.auction_price_per_unit for item in items]

            report = Report(dated_at=date)
            report.total_unit = sum([item.item_count for item in items])
            report.max_price = max(item_list)
            report.low_price = min(item_list)
            report.average_price = sum(item_list) / len(item_list)
            reports.append(report)

        return reports

    @DeprecationWarning
    def get_statistics_string(self, statistics):
        # 헤더와 구분선 정의
        lines = [
            f"{'일시':<20}{'최고가':<10}{'최저가':<10}",
            "-" * 40
        ]

        # 데이터 추가
        for item in statistics:
            date = item['일시']
            max_price = item['최고가']
            min_price = item['최저가']
            lines.append(f"{date:<20}{max_price:<10}{min_price:<10}")

        # 리스트를 문자열로 병합하여 반환
        return "\n".join(lines)
