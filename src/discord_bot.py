import datetime
import os
import pandas as pd
import discord
from discord.ext import tasks
from dotenv import load_dotenv

from adapter.mabinogi.mabinogi_client import MabinogiClient
from com.define.auction_target_itme import AutionTargetItem
from com.define.auction_processor import AutionPreProcess

load_dotenv()

CHANNEL_1 = os.environ['DISCORD_CHANNEL_1']
DISCORD_CHANNEL_2 = os.environ['DISCORD_CHANNEL_2']
DISCORD_CHANNEL_3 = os.environ['DISCORD_CHANNEL_3']
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

        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)

        channel = self.get_channel(int(CHANNEL_1))
        if channel:
            await channel.send(content=f"{datetime.date.today()}:검쨩봇 일어나다.")

        self.batch.start()
        self.batch2.start()

    @tasks.loop(seconds=3600)
    async def batch(self):
        try:
            channel = self.get_channel(int(DISCORD_CHANNEL_2))
            if channel:
                await channel.send(content=f"조회 시점 : {datetime.datetime.now()}")

                await channel.send(content=f"\n\n크롬바스 갈래말래?")
                rows = []
                for k, v in self.collect_chrombars().items():
                    rows.append({
                        "아이템명": k,
                        "최저가": v["최저가"],
                        "평균가": v["평균가"],
                        "최고가": v["최고가"]
                    })

                df = pd.DataFrame(rows, columns=["아이템명", "최저가", "평균가", "최고가"])
                await channel.send(content=df.to_markdown())
                await channel.send(content="-" * 50)

        except Exception as e:
            print(e)

    @tasks.loop(seconds=1800)
    async def batch2(self):
        try:
            channel = self.get_channel(int(DISCORD_CHANNEL_3))
            if channel:
                await channel.send(content=f"조회 시점 : {datetime.datetime.now()}")
                await channel.send(content=f"\n\n물교 할래말래?")

                rows = []
                for k, v in self.collect_barters().items():
                    rows.append({
                        "아이템명": k,
                        "최저가": v["최저가"],
                        "평균가": v["평균가"],
                        "최고가": v["최고가"]
                    })
                df = pd.DataFrame(rows, columns=["아이템명", "최저가", "평균가", "최고가"])

                await channel.send(content=df.to_markdown())
                await channel.send(content="-" * 50)
        except Exception as e:
            print(e)

    def collect_barters(self):
        barters = AutionTargetItem.get_barter()
        summary = {}
        for barter in barters:
            response = self.mabinogi_client.get_auction_items(item_name=barter.item_name,
                                                              item_category=barter.auction_item_category)
            result = AutionPreProcess.get_price_summary(response)
            summary[barter.item_name] = result
        return summary

    def collect_chrombars(self):
        barters = AutionTargetItem.get_chromebars()
        summary = {}
        for barter in barters:
            response = self.mabinogi_client.get_auction_items(item_name=barter.item_name,
                                                              item_category=barter.auction_item_category)
            result = AutionPreProcess.get_price_summary(response)
            summary[barter.item_name] = result
        return summary


if __name__ == '__main__':
    client = MyClient(
        mabinogi_client=MabinogiClient(
            api_key=MABINOGI_API_TOKEN
        )
    )
    client.run(os.environ['DISCORD_TOKEN'])
