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
from mabinogi.processor.extractor.mabinogi_ohlc_extractor import MabinogiPriceExtractor
from mabinogi.processor.sorter import MabinogiAuctionItemSorter
from render.html_image_exporter import HtmlImageExporter
from render.html_render import HtmlRender

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

mabinogi_client = MabinogiClient(api_key=os.environ['NEXON_API_TOKEN'])

item = mabinogi_items.test_items()[0]

acution_items = mabinogi_client.get_auction_items(item)

market_data = MabinogiTimeProcessor(auction_items=acution_items) \
    .get_auction_item_group_by_minutes()

cc = MabinogiPriceExtractor(market_data)

from pprint import pprint
pprint(cc.get_price())
