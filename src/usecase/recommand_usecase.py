import random
from typing import List

from numpy.distutils.system_info import atlas_version_c_text

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.entity.collect import Collect
from src.entity.location import Location
from src.repository.collection_repository import CollectRepository
from src.repository.location_repository import LocationRepository

from adapter.mabinogi.mabinogi_client import MabinogiClient
from src.service.auction_item_metrics_service import AuctionItemsMetricsService
from src.service.discord_service import DiscordService
from src.usecase.dto.recommand_items import RecommandItemsDto


class RecommandUsecase:

    def __init__(self, collect_repo, location_repo, mabinogi_client):
        self.collect_repo: CollectRepository = collect_repo
        self.location_repo: LocationRepository = location_repo
        self.mabinogi_client: MabinogiClient = mabinogi_client
        self.discord_service = DiscordService()

    def fetch_by(self, item: Collect) -> List[AuctionItemDto]:
        """ 마비노기 클라이언트에 입력 아이템으로 경매장 검색 """
        auction_items: List[AuctionItemDto] = self.mabinogi_client.get_auction_items(
            item_category=item.category,
            item_name=item.name
        )
        return auction_items[0:5]

    def execute(self) -> str:
        """ 임의의 장소를 랜덤으로 선택한 뒤, 해당 장소에서 얻을 수 있는 아이템 정보를 추천함 """
        pick_random_location: Location = random.choice(self.location_repo.get_all_location())

        collections = self.collect_repo.find_collect_by_location_id(location_id=pick_random_location.location_id)
        if not collections:
            raise Exception("Collect 정보를 찾을 수 없음")

        results = []
        for collect in collections:
            aution_items = self.fetch_by(collect)

            metric = AuctionItemsMetricsService(aution_items)
            result = self.to_dto(
                location=pick_random_location.name,
                item_name=collect.name,
                item_per_minute=collect.time_per_minute,
                item_per_count=collect.time_per_count,
                avg_price=metric.average(),
                total_count=metric.size(),
                expect=metric.calculate_hourly_revenue(
                    collect.time_per_minute,
                    collect.time_per_count
                )

            )
            results.append(result.to_stat_dict())

        return self.discord_service.execute(results)

    def to_dto(self, location, item_name, item_per_minute, item_per_count, avg_price, total_count, expect):
        return RecommandItemsDto(
            location=location,
            item_name=item_name,
            item_per_minute=item_per_minute,
            item_per_count=item_per_count,
            avg_price=avg_price,
            total_count=total_count,
            expect=expect
        )
