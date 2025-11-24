import os

from adapter.mabinogi.mabinogi_client import MabinogiClient
from src.db.mabinogi_db_connector import MabinogiDbConnector
from src.repository.collection_repository import CollectRepository
from src.repository.location_repository import LocationRepository
from src.usecase.recommand_usecase import RecommandUsecase

from dotenv import load_dotenv

load_dotenv()


class TestSourceCode:
    def __init__(self):
        connector = MabinogiDbConnector()

    def test(self):
        with MabinogiDbConnector() as connector:
            self.collect_repo = CollectRepository(connector)
            collect = self.collect_repo.find_collect_by_name(name="순수의 결정")
            print(collect)


if __name__ == '__main__':
    with MabinogiDbConnector() as connector:
        repo = CollectRepository(connector)
        location_repo = LocationRepository(connector)

        mabinogi_client = MabinogiClient(
            api_key=os.environ["MABINOGI_API_KEY"]
        )

        usecase = RecommandUsecase(repo, location_repo, mabinogi_client)
        r = usecase.execute()

        print(r)


