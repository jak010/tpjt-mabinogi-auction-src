import os

import discord
import pandas as pd
from discord.ext import tasks
from dotenv import load_dotenv

from adapter.mabinogi.mabinogi_client import MabinogiClient
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


class MyClient(discord.Client):

    def __init__(self,
                 mabinogi_client
                 ):
        self.mabinogi_client = mabinogi_client
        self.target_channel = int(GUILD_CHANNEL)

        self.storage = TrackStorage()

        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)


        self.batch.start()

    @tasks.loop(seconds=1800)
    async def batch(self):
        try:
            channel = self.get_channel(self.target_channel)

            recommend_service = RecommendService(
                mabinogi_client=self.mabinogi_client,
                recommend_items=self.storage.get_money()
            )

            await channel.send(recommend_service.get_summary())

        except Exception as e:
            print(e)


if __name__ == '__main__':
    client = MyClient(
        mabinogi_client=MabinogiClient(
            api_key=MABINOGI_API_TOKEN
        )
    )
    client.run(os.environ['DISCORD_TOKEN'])
