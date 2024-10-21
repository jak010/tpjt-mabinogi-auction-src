import json
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from mabinogi import mabinogi_items
from mabinogi.mabinogi_client import MabinogiClient
from mabinogi.processor.mabinogi_auction_item_processor import MabinogiAuctionItemProcessor
from mabinogi.processor.mabinogi_data_processor import MabinogiDataProcessor
from mabinogi.processor.mabinogi_time_processor import MabinogiTimeProcessor
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
            # channel = self.get_channel(int(DiscordChannel.CHANNEL_1.value))

            for tracking_item in mabinogi_items.get_items():
                acution_items = self.mabinogi_client.get_auction_items(tracking_item)

                acution_items_in_today = MabinogiTimeProcessor(acution_items) \
                    .get_auction_item_with_two_days()
                get_auction_items_group_by_hourly = MabinogiAuctionItemProcessor(auction_items=acution_items_in_today) \
                    .get_auction_items_group_by_hourly()

                sorted_auction_items_group_by_hourly = {k: v for k, v in
                                                        sorted(get_auction_items_group_by_hourly.items(), key=lambda x: x, reverse=True)}

                action_reports = MabinogiDataProcessor(auction_items=sorted_auction_items_group_by_hourly) \
                    .get_report()

                action_reports_to_json = [json.loads(json.dumps(action_report.as_dict())) for action_report in sorted(action_reports)]

                render = HtmlRender(
                    title=tracking_item.item_name,
                    reports=action_reports,
                    reports_json=action_reports_to_json
                )
                render.execute()

                exporter = HtmlImageExporter()
                exporter.execute()

                # await channel.send(file=DiscordFile(exporter.save_path()))

        except Exception as e:
            raise e


if __name__ == '__main__':
    client = MyClient()
    client.run(
        os.environ['DISCORD_TOKEN']
    )
