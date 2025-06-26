import unittest

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item


class TestMabinogiClient(unittest.TestCase):
    def setUp(self):
        """
        테스트를 위한 초기 설정을 수행합니다.
        MabinogiClient 인스턴스를 생성하고 API 키, 기본 URL, 헤더를 설정합니다.
        """
        self.api_key = "test_6366e5f0ae09b2f93d90bb29f58fa0ae473283798afb130f51d5a088dfcb3b37efe8d04e6d233bd35cf2fabdeb93fb0d"
        self.client = MabinogiClient(self.api_key)
        self.base_url = "https://open.api.nexon.com"
        self.headers = {"x-nxopen-api-key": self.api_key}

    @unittest.skip("demonstrating skipping")
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

    @unittest.skip("demonstrating skipping")
    def test_get_auction_items_success_2(self):
        """
        여러 경매장 아이템에 대해 get_auction_items 메서드가 성공적으로 작동하는지 테스트합니다.
        각 아이템에 대해 API를 호출하고 반환된 객체가 AuctionItemDto 인스턴스인지 확인합니다.
        """

        auction_items = [
            Item(auction_item_category="기타", item_name="순수의 결정"),
            Item(auction_item_category="포션", item_name="크라반의 수액")
        ]

        for auction_item in auction_items:

            fetched_auction_item = self.client.get_auction_items(
                item=auction_item
            )

            for fetched_auction_ite in fetched_auction_item:
                assert isinstance(fetched_auction_ite, AuctionItemDto)

    def test_get_auction_items_success_3(self):
        """
        여러 경매장 아이템에 대해 get_auction_items 메서드가 성공적으로 작동하는지 테스트합니다.
        각 아이템에 대해 API를 호출하고 반환된 객체가 AuctionItemDto 인스턴스인지 확인합니다.
        """

        auction_items = [
            Item(auction_item_category="기타", item_name="순수의 결정"),
            Item(auction_item_category="포션", item_name="크라반의 수액")
        ]

        for auction_item in auction_items:
            fetched_auction_item = self.client.get_auction_items(
                item=auction_item,
                days=1
            )
            print(fetched_auction_item)


if __name__ == '__main__':
    unittest.main()
