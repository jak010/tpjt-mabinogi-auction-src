import operator
import os

from mabinogi.mabinogi_client import MabinogiClient
from mabinogi.mabinogi_processor import MabinogiProcessor
from mabinogi import mabinogi_items
from mabinogi.model.Item import Item
from dotenv import load_dotenv

from model.AuctionHistoryDto import AuctionHistoryDto

load_dotenv()

mabinogi_client = MabinogiClient(api_key=os.environ['NEXON_API_TOKEN'])
mabinogi_processor = MabinogiProcessor()


def get_auction_histories():
    auction_items = mabinogi_client.get_auction_hsitory_items(
        item=Item(
            auction_item_category="천옷/방직",
            item_name="고급 가죽"
        )
    )
    for auction_item in auction_items:
        print(auction_item)


def group_by_acution_histories():
    import json

    auction_items = []
    with open("dataset.json") as file:
        dataset = json.loads(file.read())
        [auction_items.append(AuctionHistoryDto(**item)) for item in dataset["auction_history"]]


    group_by_items = mabinogi_processor.get_auction_history_group_by_hourly(auction_items)
    statistics = {}
    from collections import defaultdict
    statistics_by_time = defaultdict(list)
    for k, v in group_by_items.items():

        for item in v:
            statistics_by_time[item.auction_price_per_unit].append(item.get_date_auction_buy_kst())

            if item.auction_price_per_unit not in statistics:
                statistics[item.auction_price_per_unit] = item.item_count
            else:
                statistics[item.auction_price_per_unit] += item.item_count
    from pprint import pprint
    pprint(statistics_by_time)


if __name__ == '__main__':
    # c = {33333: 9, 33000: 113, 34500: 59, 32000: 37, 34000: 298, 33400: 7, 30000: 8, 32900: 32, 33800: 10, 32899: 3, 31000: 30, 31467: 15, 35000: 5,
    #      34444: 32, 33332: 1, 34999: 60, 33999: 5, 34900: 10, 33222: 10, 31500: 14, 33500: 120, 31900: 2}
    #
    # d = sorted(c.items(), key=lambda x: x[1])
    # print(d)

    group_by_acution_histories()
