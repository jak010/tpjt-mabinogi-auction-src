# MabinogiDbConnector 사용법

`MabinogiDbConnector` 클래스는 `pymysql`을 사용하여 MySQL 데이터베이스에 연결하고 데이터를 쿼리 및 업데이트하며 트랜잭션을 관리하는 기능을 제공합니다.

## 1. 클래스 초기화

`MabinogiDbConnector` 클래스는 데이터베이스 연결 정보를 인자로 받습니다. 기본값은 `docker-compose.yml` 파일에 정의된 정보를 따릅니다.

```python
from src.db.mabinogi_db_connector import MabinogiDbConnector

# 기본값으로 초기화 (localhost:51122, user=root, password=1234, db=mabinogi)
db_connector = MabinogiDbConnector()

# 또는 사용자 정의 연결 정보로 초기화
# db_connector = MabinogiDbConnector(
#     host='your_host',
#     port=3306,
#     user='your_user',
#     password='your_password',
#     db='your_database'
# )
```

## 2. 데이터베이스 연결 및 해제

`connect()` 메서드를 사용하여 데이터베이스에 연결하고, `disconnect()` 메서드를 사용하여 연결을 해제합니다.

```python
db_connector = MabinogiDbConnector()
try:
    db_connector.connect()
    print("데이터베이스에 성공적으로 연결되었습니다.")
    # 데이터베이스 작업 수행
except Exception as e:
    print(f"연결 오류: {e}")
finally:
    db_connector.disconnect()
    print("데이터베이스 연결이 해제되었습니다.")
```

### 컨텍스트 매니저 사용 (권장)

`with` 문을 사용하여 컨텍스트 매니저로 활용하면, 연결이 자동으로 관리되어 편리합니다.

```python
with MabinogiDbConnector() as db_connector:
    print("데이터베이스에 성공적으로 연결되었습니다.")
    # 데이터베이스 작업 수행
print("데이터베이스 연결이 자동으로 해제되었습니다.")
```

## 3. 쿼리 실행 (SELECT)

`execute_query(query, params=None)` 메서드를 사용하여 데이터를 조회합니다. 결과는 딕셔너리 형태로 반환됩니다.

```python
with MabinogiDbConnector() as db_connector:
    try:
        # 모든 데이터 조회 예시
        results = db_connector.execute_query("SELECT * FROM your_table_name LIMIT 5")
        for row in results:
            print(row)

        # 조건부 데이터 조회 예시
        results_with_params = db_connector.execute_query(
            "SELECT * FROM your_table_name WHERE id = %s", (1,)
        )
        print(results_with_params)

    except ConnectionError as e:
        print(f"연결 오류: {e}")
    except Exception as e:
        print(f"쿼리 실행 오류: {e}")
```

## 4. 데이터 업데이트 (INSERT, UPDATE, DELETE)

`execute_update(query, params=None)` 메서드를 사용하여 데이터를 삽입, 업데이트 또는 삭제합니다. 변경된 행의 수를 반환합니다. 이 메서드는 트랜잭션 내에서 호출되어야 합니다.

```python
with MabinogiDbConnector() as db_connector:
    try:
        db_connector.begin_transaction()

        # 데이터 삽입 예시
        insert_query = "INSERT INTO your_table_name (name, value) VALUES (%s, %s)"
        row_count = db_connector.execute_update(insert_query, ("Test Item", 100))
        print(f"삽입된 행 수: {row_count}")

        # 데이터 업데이트 예시
        update_query = "UPDATE your_table_name SET value = %s WHERE name = %s"
        row_count = db_connector.execute_update(update_query, (150, "Test Item"))
        print(f"업데이트된 행 수: {row_count}")

        # 데이터 삭제 예시
        delete_query = "DELETE FROM your_table_name WHERE name = %s"
        row_count = db_connector.execute_update(delete_query, ("Test Item",))
        print(f"삭제된 행 수: {row_count}")

        db_connector.commit_transaction()
        print("트랜잭션이 성공적으로 커밋되었습니다.")

    except ConnectionError as e:
        print(f"연결 오류: {e}")
    except Exception as e:
        print(f"업데이트 실행 오류: {e}")
        db_connector.rollback_transaction()
        print("트랜잭션이 롤백되었습니다.")
```

## 5. 트랜잭션 관리

`begin_transaction()`, `commit_transaction()`, `rollback_transaction()` 메서드를 사용하여 명시적으로 트랜잭션을 제어할 수 있습니다.

```python
db_connector = MabinogiDbConnector()
try:
    db_connector.connect()
    db_connector.begin_transaction()

    # 여러 업데이트 작업 수행
    db_connector.execute_update("INSERT INTO another_table (col) VALUES (%s)", ("data1",))
    db_connector.execute_update("UPDATE yet_another_table SET col = %s WHERE id = %s", ("data2", 1))

    # 모든 작업이 성공하면 커밋
    db_connector.commit_transaction()
    print("모든 트랜잭션이 성공적으로 커밋되었습니다.")

except ConnectionError as e:
    print(f"연결 오류: {e}")
except Exception as e:
    print(f"트랜잭션 오류: {e}")
    # 오류 발생 시 롤백
    db_connector.rollback_transaction()
    print("트랜잭션이 롤백되었습니다.")
finally:
    db_connector.disconnect()
```

## 6. Repository 패턴 사용 예시

`MabinogiDbConnector`는 저수준의 데이터베이스 연결 및 쿼리 실행을 담당하며, `MabinogiAuctionRepository`와 같은 Repository 클래스에서 이를 주입받아 특정 도메인 객체(예: `AuctionItemDto`)에 대한 CRUD 작업을 수행할 수 있습니다.

```python
from src.db.mabinogi_db_connector import MabinogiDbConnector
from src.repository.mabinogi_auction_repository import MabinogiAuctionRepository
from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from datetime import datetime, timezone, timedelta

# 1. DbConnector 인스턴스 생성
db_connector = MabinogiDbConnector()

# 2. Repository 인스턴스 생성 시 DbConnector 주입
auction_repository = MabinogiAuctionRepository(db_connector)

# 3. Repository 메서드 사용 예시
try:
    db_connector.connect()
    db_connector.begin_transaction()

    # 새로운 AuctionItemDto 생성
    new_item = AuctionItemDto(
        item_name="테스트 아이템",
        item_display_name="테스트 아이템 (표시)",
        item_count=1,
        auction_price_per_unit=10000,
        date_auction_expire=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat().replace('+00:00', 'Z'),
        auction_item_category="무기",
        item_option=[{"type": "강화", "value": "10"}]
    )

    # 아이템 추가
    row_count = auction_repository.add_auction_item(new_item)
    print(f"추가된 아이템 수: {row_count}")

    # 아이템 조회
    items = auction_repository.get_auction_item_by_name("테스트 아이템")
    for item in items:
        print(f"조회된 아이템: {item}")

    # 모든 아이템 조회
    all_items = auction_repository.get_all_auction_items()
    print(f"총 아이템 수: {len(all_items)}")

    db_connector.commit_transaction()
    print("Repository 작업을 포함한 트랜잭션이 성공적으로 커밋되었습니다.")

except ConnectionError as e:
    print(f"데이터베이스 연결 오류: {e}")
except Exception as e:
    print(f"Repository 작업 중 오류 발생: {e}")
    db_connector.rollback_transaction()
    print("Repository 작업을 포함한 트랜잭션이 롤백되었습니다.")
finally:
    db_connector.disconnect()
