import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from adapter.mabinogi.mabinogi_client import MabinogiClient
from src.db.mabinogi_db_connector import MabinogiDbConnector
from src.repository.collection_repository import CollectRepository
from src.repository.location_repository import LocationRepository
from src.usecase.recommand_usecase import RecommandUsecase

load_dotenv()

MABINOGI_API_TOKEN = os.environ['MABINOGI_API_KEY']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GUILD_CHANNEL = os.environ["BIRTH_DAY"]

intents = discord.Intents.default()
intents.message_content = True


class MabinogiDiscordClient(discord.Client):
    MESSAGE_TARGET_CHANNEL = int(GUILD_CHANNEL)

    def __init__(self, usecase: RecommandUsecase):
        self.usecase = usecase

        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)

        self.batch.start()

    @tasks.loop(seconds=900)  # 15분마다 실행
    async def batch(self):
        try:
            channel = self.get_channel(self.MESSAGE_TARGET_CHANNEL)
            if channel:
                await channel.send(self.usecase.execute())

                print(f"Message sent to channel {self.MESSAGE_TARGET_CHANNEL} at {discord.utils.utcnow()}")
            else:
                print(f"Channel {self.MESSAGE_TARGET_CHANNEL} not found.")
        except Exception as e:
            print(f"Error in batch task: {e}")


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True  # 메시지 콘텐츠 인텐트 활성화

    with MabinogiDbConnector() as connector:
        repo = CollectRepository(connector)
        location_repo = LocationRepository(connector)
        mabinogi_client = MabinogiClient(api_key=MABINOGI_API_TOKEN)

        client = MabinogiDiscordClient(
            usecase=RecommandUsecase(
                CollectRepository(connector),
                LocationRepository(connector),
                MabinogiClient(api_key=MABINOGI_API_TOKEN)
            )
        )
        client.run(DISCORD_TOKEN)
