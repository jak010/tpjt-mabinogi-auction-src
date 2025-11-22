from typing import List

import json
from bot.dto.auction_item import AuctionItem
from bot.dto.money_item import MoneyItem


class TrackStorage:

    def __init__(self):
        self.content = ""

    def get_baters(self) -> List[AuctionItem]:
        result = []
        for barter in self.content["baters"]:
            result.append(
                AuctionItem(
                    name=barter["name"],
                    category=barter["category"]
                )
            )
        return result

    def get_money(self) -> List[MoneyItem]:
        with open("./storage/recommand_items.json", "r") as f:
            self.content = json.load(f)

            result = []
            for money in self.content["items"]:
                result.append(
                    MoneyItem(
                        name=money["name"],
                        category=money["category"],
                        time_per_minute=money["time_per_minute"],
                        time_per_count=money["time_per_count"],
                        is_searchable=money["is_searchable"]
                    )
                )
            return result
