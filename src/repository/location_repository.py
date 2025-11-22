from typing import List, Dict, Optional
from src.db.mabinogi_db_connector import MabinogiDbConnector
from src.entity.location import Location
from datetime import datetime


class LocationRepository:
    def __init__(self, db_connector: MabinogiDbConnector):
        self.db_connector = db_connector

    def add_location(self, code: str, name: str) -> int:
        """새로운 위치를 locations 테이블에 추가하고, 생성된 location_id를 반환합니다."""
        query = """
        INSERT INTO locations (code, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name)
        """
        params = (code, name)
        self.db_connector.execute_update(query, params)

        # 중복 키 업데이트 시에도 ID를 가져오기 위해 다시 조회
        select_query = "SELECT location_id FROM locations WHERE code = %s"
        result = self.db_connector.execute_query(select_query, (code,))
        return result[0]['location_id'] if result else None

    def get_location_by_code(self, code: str) -> Optional[Location]:
        """code로 위치 정보를 조회합니다."""
        query = "SELECT * FROM locations WHERE code = %s"
        rows = self.db_connector.execute_query(query, (code,))
        if rows:
            row = rows[0]
            return Location(
                location_id=row['location_id'],
                code=row['code'],
                name=row['name'],
                created_at=row['created_at']
            )
        return None

    def get_location_by_id(self, location_id: int) -> Optional[Location]:
        """location_id로 위치 정보를 조회합니다."""
        query = "SELECT * FROM locations WHERE location_id = %s"
        rows = self.db_connector.execute_query(query, (location_id,))
        if rows:
            row = rows[0]
            return Location(
                location_id=row['location_id'],
                code=row['code'],
                name=row['name'],
                created_at=row['created_at']
            )
        return None

    def get_all_locations(self) -> List[Location]:
        """모든 위치 정보를 조회합니다."""
        query = "SELECT * FROM locations;"
        rows = self.db_connector.execute_queries(query)
        return [
            Location(
                location_id=row.get("location_id"),
                code=row['code'],
                name=row['name'],
                created_at=row['created_at']
            ) for row in rows
        ]
