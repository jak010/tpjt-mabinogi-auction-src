import json
import os
from datetime import datetime

import discord
from discord import File
from discord.ext import tasks
from dotenv import load_dotenv
from html2image import Html2Image
from jinja2 import Template

from discordlib.channel import DiscordChannel
from mabinogi.mabinogi_client import MabinogiClient
from mabinogi.mabinogi_processor import MabinogiProcessor
from mabinogi import mabinogi_items
from pathlib import Path

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):

    def __init__(self,
                 mabinogi_client,
                 mabinogi_processor
                 ):
        self.mabinogi_client = mabinogi_client
        self.mabinogi_processor: MabinogiProcessor = mabinogi_processor

        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online)
        await self.batch.start()

    @tasks.loop(seconds=60)
    async def batch(self):
        try:
            channel = self.get_channel(DiscordChannel.CHANNEL_1.value)

            for tracking_item in mabinogi_items.get_items():
                acution_items = self.mabinogi_client.get_auction_items(tracking_item)

                acution_items_in_today = self.mabinogi_processor.get_auction_item_in_today(acution_items)
                get_auction_items_group_by_hourly = self.mabinogi_processor.get_auction_items_group_by_hourly(auction_items=acution_items_in_today)

                sorted_auction_items_group_by_hourly = {k: v for k, v in
                                                        sorted(get_auction_items_group_by_hourly.items(), key=lambda x: x, reverse=True)}
                action_reports = self.mabinogi_processor.get_report(auction_items=sorted_auction_items_group_by_hourly)
                action_reports_to_json = [json.loads(json.dumps(action_report.as_dict())) for action_report in sorted(action_reports)]

                with open("./templates/report.html", "r") as f:
                    template = Template(f.read())

                    html_content = template.render(
                        title=tracking_item.item_name,
                        reports=self.mabinogi_processor.get_report(auction_items=get_auction_items_group_by_hourly),
                        reports_json=action_reports_to_json,
                        date=datetime.now().strftime('%Y-%m-%d')
                    )
                    with open("./temp.html", "w", encoding="utf-8") as f2:
                        f2.write(html_content)

                with open("./temp.html") as f:
                    htoi = Html2Image()
                    htoi.screenshot(
                        f.read(),
                        size=(1200, 1200),
                        css_str=Path("./templates/style.css").read_text(),
                        save_as="out.png"
                    )

                await channel.send(file=File("./out.png"))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    client = MyClient(
        mabinogi_client=MabinogiClient(api_key=os.environ['NEXON_API_TOKEN']),
        mabinogi_processor=MabinogiProcessor(),

    )
    client.run(os.environ['DISCORD_TOKEN'])
