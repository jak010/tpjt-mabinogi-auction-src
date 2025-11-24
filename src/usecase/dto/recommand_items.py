import json
from dataclasses import dataclass


@dataclass
class RecommandItemsDto:
    location: str  # 위치
    item_name: str  # 아이템명
    item_per_minute: int  # 단위(분)
    item_per_count: int  # 기대 획득 수
    avg_price: float  # 경매장 최저 5개의 평균가격
    total_count: int  # 매물 수
    expect: float  # 1시간 기대 수익률

    def __str__(self):
        return f"location: {self.location}, item_name: {self.item_name}, item_per_minute: {self.item_per_minute}, item_per_count: {self.item_per_count}, avg_price: {self.avg_price}, total_count: {self.total_count}, expect: {self.expect}"

    def to_stat_dict(self):
        """주석 정보를 키로 사용하여 값 반환"""
        return json.dumps({
            "위치": self.location,
            "아이템명": self.item_name,
            "단위(분)": self.item_per_minute,
            "기대 획득 수": self.item_per_count,
            "경매장 최저 5개의 평균가격": self.avg_price,
            "매물 수": self.total_count,
            "1시간 기대 수익률": self.expect
        })
