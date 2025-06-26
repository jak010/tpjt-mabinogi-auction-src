import unittest

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item


# def test_items() -> List[Item]:
#     return [
#
#         Item(
#             auction_item_category="기타",
#             item_name="순수의 결정"
#         ),
#         Item(
#             auction_item_category="포션",
#             item_name="크라반의 수액"
#         )
#     ]

class TestMabinogiClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_6366e5f0ae09b2f93d90bb29f58fa0ae473283798afb130f51d5a088dfcb3b37efe8d04e6d233bd35cf2fabdeb93fb0d"
        self.client = MabinogiClient(self.api_key)
        self.base_url = "https://open.api.nexon.com"
        self.headers = {"x-nxopen-api-key": self.api_key}
        self.test_item = {
            "auction_item_category": "의류",
            "item_name": "원더랜드 드레스"
        }

    def test_get_auction_items_success(self):
        # Call the method

        items = self.client.get_auction_items(
            item=Item(
                auction_item_category="천옷/방직",
                item_name="고급 가죽"
            )
        )

        for item in items:
            assert isinstance(item, AuctionItemDto)

        """ Sample 
        {
            'auction_item': [
                {'item_name': '고급 가죽', 'item_display_name': '고급 가죽', 'item_count': 10, 'auction_item_category': '천옷/방직', 'auction_price_per_unit': 11110, 'date_auction_expire': '2025-06-28T20:03:00.000Z', 'item_option': None},
                {'item_name': '고급 가죽', 'item_display_name': '고급 가죽', 'item_count': 10, 'auction_item_category': '천옷/방직', 'auction_price_per_unit': 20000, 'date_auction_expire': '2025-06-27T20:03:00.000Z', 'item_option': None}
            ]
        } 
        """


if __name__ == '__main__':
    unittest.main()
