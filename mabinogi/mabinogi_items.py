from typing import List

from .model.Item import Item


def get_items() -> List[Item]:
    return [
        Item(
            auction_item_category="천옷/방직",
            item_name="고급 가죽"
        ),
        Item(
            auction_item_category="기타",
            item_name="순수의 결정"
        ),
        Item(
            auction_item_category="포션",
            item_name="크라반의 수액"
        )
    ]
