import os
import discord
from discord.ext import tasks
import asyncio

from dotenv import load_dotenv

from adapter.mabinogi.mabinogi_client import MabinogiClient
from src.db.mabinogi_db_connector import MabinogiDbConnector
from src.repository.item_repository import ItemRepository
from src.repository.location_repository import LocationRepository
from src.service.recommand_service import RecommandService
from src.service.recommend_summary import get_info
from bot.guild_client import MyClient  # MyClient 임포트

load_dotenv()

MABINOGI_API_TOKEN = os.environ['MABINOGI_API_KEY']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GUILD_CHANNEL = os.environ["BIRTH_DAY"]

intents = discord.Intents.default()
intents.message_content = True


class MabinogiDiscordClient(discord.Client):
    def __init__(self, recommand_service: RecommandService, mabinogi_client: MabinogiClient):

        self.mabinogi_client = mabinogi_client
        self.recommand_service = recommand_service

        self.target_channel = int(GUILD_CHANNEL)

        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)

        self.batch.start()

    @tasks.loop(seconds=900)  # 15분마다 실행
    async def batch(self):
        try:
            channel = self.get_channel(self.target_channel)
            if channel:

                r = self.recommand_service.execute()


                recommendation_info = get_info(self.recommand_service.execute())
                await channel.send(recommendation_info)

                print(f"Message sent to channel {self.target_channel} at {discord.utils.utcnow()}")
            else:
                print(f"Channel {self.target_channel} not found.")
        except Exception as e:
            print(f"Error in batch task: {e}")


if __name__ == "__main__":
    with MabinogiDbConnector() as connector:
        repo = ItemRepository(connector)
        location_repo = LocationRepository(connector)
        mabinogi_client = MabinogiClient(
            api_key=MABINOGI_API_TOKEN
        )

        recommand_service_instance = RecommandService(location_repo, repo, mabinogi_client)

        intents = discord.Intents.default()
        intents.message_content = True  # 메시지 콘텐츠 인텐트 활성화

        client = MabinogiDiscordClient(
            recommand_service=recommand_service_instance,
            mabinogi_client=mabinogi_client
        )
        client.run(DISCORD_TOKEN)
