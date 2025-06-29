import os
from typing import List

from adapter.mabinogi.mabinogi_client import MabinogiClient
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from adapter.mabinogi.model.Item import Item
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class MabinogiAuctionRepository:
    def __init__(self):
        self.client = MabinogiClient(api_key=os.environ['MABINOGI_API_KEY'])

    def get_auction_items(self, item_name: str) -> List[AuctionItemDto]:
        """
        마비노기 경매장에서 아이템을 조회합니다.
        """
        return self.client.get_auction_items(item_name=item_name)
