from typing import List
import pandas as pd

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto


class AutionPreProcess:
    @staticmethod
    def get_price_summary(auction_item: List[AuctionItemDto]) -> dict:
        if not auction_item:
            return {"min": None, "avg": None, "max": None}

        prices = [h.auction_price_per_unit for h in auction_item]

        min_price = min(prices)
        max_price = max(prices)
        avg_price = round(sum(prices) / len(prices))  # 소수점 반올림

        return {
            "최저가": min_price,
            "평균가": avg_price,
            "최고가": max_price
        }


class Test:

    def method(self):
        colums = ["아이템명", "최저가", "평균가", "최고가"]
        data = [
            ["Name", "1", "2", "3"],
            ["Name2", "1", "2", "3"],
        ]

        df = pd.DataFrame(data, columns=colums)
        print(df.to_markdown())


if __name__ == '__main__':
    t = Test()
    t.method()
