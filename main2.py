# from pathlib import Path
#
# from mabinogi.mabinogi_client import MabinogiClient
# from mabinogi.mabinogi_processor import MabinogiProcessor
# from mabinogi.model.Item import Item
#
#
# mabinogi_client = MabinogiClient()
# mabinogi_processor = MabinogiProcessor()
#
# acution_items = mabinogi_client.get_auction_items_test(
#     Item(
#         auction_item_category="천옷/방직",
#         item_name="고급 가죽"
#     )
# )
#
# acution_items_in_today = mabinogi_processor.get_auction_item_in_today(acution_items)
# get_auction_items_group_by_hourly = mabinogi_processor.get_auction_items_group_by_hourly(auction_items=acution_items_in_today)
# import json
#
# sorted_auction_items_group_by_hourly = {k: v for k, v in sorted(get_auction_items_group_by_hourly.items(), key=lambda x: x, reverse=True)}
# action_reports = mabinogi_processor.get_report(auction_items=sorted_auction_items_group_by_hourly)
# action_reports_to_json = [json.loads(json.dumps(action_report.as_dict())) for action_report in sorted(action_reports)]
#
# from datetime import datetime
# from html2image import Html2Image
# from jinja2 import Template
#
# with open("./templates/report2.html", "r") as f:
#     template = Template(f.read())
#
#     html_content = template.render(
#         title="고급 가죽",
#         reports=mabinogi_processor.get_report(auction_items=sorted_auction_items_group_by_hourly),
#         reports_json=action_reports_to_json,
#         date=datetime.now().strftime('%Y-%m-%d')
#     )
#
#     with open("./test2.html", "w", encoding="utf-8") as f2:
#         f2.write(html_content)
#
# css_Str = Path("./templates/style.css").read_text()
# htoi = Html2Image()
# with open("./test2.html") as f:
#     htoi.screenshot(
#         f.read(),
#         css_str=css_Str,
#         save_as="out.png"
#     )
