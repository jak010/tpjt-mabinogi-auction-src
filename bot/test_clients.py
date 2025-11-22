import os

import discord
import pandas as pd
from dotenv import load_dotenv

from adapter.mabinogi.mabinogi_client import MabinogiClient
from bot.dto.money_item import MoneyItem
from bot.service import GoogleLLM
from bot.service.recommend_service import RecommendService
from bot.storage.track_storage import TrackStorage

load_dotenv()

GUILD_CHANNEL = os.environ["BIRTH_DAY"]
MABINOGI_API_TOKEN = os.environ['MABINOGI_API_KEY']

intents = discord.Intents.default()
intents.message_content = True

pd.set_option("display.colheader_justify", "center")  # 헤더 중앙정렬
pd.set_option("display.width", None)  # 줄바꿈 방지
pd.set_option("display.unicode.east_asian_width", True)  # 한글 맞춤


class MyClient:

    def __init__(self,
                 mabinogi_client
                 ):
        self.mabinogi_client = mabinogi_client
        self.target_channel = int(GUILD_CHANNEL)

        self.storage = TrackStorage()

    def tet(self):
        result = self.mabinogi_client.get_auction_items(
            item_category="포션",
            item_name="크라반의 수액"
        )

        money_item1 = MoneyItem(
            category="기타",
            name="순수의 결정",
            time_per_minute=10,
            time_per_count=12,
            is_searchable=True
        )
        c = RecommendService(mabinogi_client=self.mabinogi_client, recommend_items=result)

        r1 = c.get_summary_with_items(money_item1, result)
        print(r1)

        # GoogleLLM.execute(r1)


if __name__ == '__main__':
    client = MyClient(
        mabinogi_client=MabinogiClient(
            api_key=MABINOGI_API_TOKEN
        )
    )
    client.tet()
