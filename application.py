import json
import os

import discord
from discord import File as DiscordFile
from discord.ext import tasks
from dotenv import load_dotenv

from discordlib.channel import DiscordChannel
from mabinogi import mabinogi_items
from mabinogi.mabinogi_client import MabinogiClient
from mabinogi.processor.mabinogi_auction_item_processor import MabinogiAuctionItemProcessor
from mabinogi.processor.mabinogi_data_processor import MabinogiReportProcessor
from mabinogi.processor.mabinogi_time_processor import MabinogiTimeProcessor
from mabinogi.processor.sorter import MabinogiAuctionItemSorter
from render.html_image_exporter import HtmlImageExporter
from render.html_render import HtmlRender

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):
    mabinogi_client = MabinogiClient(api_key=os.environ['NEXON_API_TOKEN'])

    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)
        await self.batch.start()

    @tasks.loop(seconds=60 * 10)
    async def batch(self):
        try:
            channel = self.get_channel(int(DiscordChannel.CHANNEL_1.value))

            # for tracking_item in mabinogi_items.get_items():
            #     acution_items = self.mabinogi_client.get_auction_items(tracking_item)
            #
            #     acution_items_until_two_day = MabinogiTimeProcessor(auction_items=acution_items) \
            #         .get_auction_item_until_two_days()
            #     auction_items_group_by_hourly = MabinogiAuctionItemProcessor(auction_items=acution_items_until_two_day) \
            #         .get_auction_items_group_by_hourly()
            #
            #     auction_reports = MabinogiReportProcessor(
            #         sorter=MabinogiAuctionItemSorter(auction_items_group_by_hourly)
            #     ).execute()
            #
            #     render = HtmlRender(
            #         title=tracking_item.item_name,
            #         reports=auction_reports[0:25],
            #         reports_json=[json.loads(json.dumps(action_report.as_dict())) for action_report in auction_reports[0:30]]
            #     )
            #     render.execute()
            #
            #     exporter = HtmlImageExporter()
            #     exporter.execute()
            #
            #     await channel.send(file=DiscordFile(exporter.save_path()))

        except Exception as e:
            raise e


if __name__ == '__main__':
    client = MyClient()
    client.run(
        os.environ['DISCORD_TOKEN']
    )
