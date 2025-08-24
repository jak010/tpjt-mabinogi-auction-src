from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionHistoryDto import AuctionHistoryDto
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item

class AutionTargetItem:

    @staticmethod
    def get_barter():
        """ 물물교환 아이템 """
        return [
            Item(
                auction_item_category="천옷/방직",
                item_name="고급 가죽"
            ),
            Item(
                auction_item_category="천옷/방직",
                item_name="최고급 가죽"
            ),
            Item(
                auction_item_category="기타",
                item_name="중급 나무장작"
            ),
            # Item(
            #     auction_item_category="포션",
            #     item_name="생명력 500 포션"
            # ),
            # Item(
            #     auction_item_category="포션",
            #     item_name="마나 500 포션"
            # ),
            # Item(
            #     auction_item_category="포션",
            #     item_name="스태미나 500 포션"
            # ),
            # Item(
            #     auction_item_category="포션",
            #     item_name="마리오네트 500 포션"
            # )
        ]

    @staticmethod
    def get_chromebars():
        """ 크롬바스 아이템 """
        return [
            Item(
                auction_item_category="기타",
                item_name="손상된 글라스 기브넨의 깃털"
            ),
            Item(
                auction_item_category="기타",
                item_name="글라스 기브넨의 심장"
            ),
            Item(
                auction_item_category="기타",
                item_name="아다만티움"
            ),
            Item(
                auction_item_category="기타",
                item_name="결정화된 겨울의 잔해"
            )
        ]