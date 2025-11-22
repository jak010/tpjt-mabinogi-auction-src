# 마비노기 경매장 데이터 분석 및 추천 시스템

이 프로젝트는 인기 온라인 게임 마비노기의 경매장 데이터를 수집, 분석하여 사용자에게 유용한 정보를 제공하는 시스템입니다. 웹 인터페이스와 Discord 봇을 통해 경매 아이템의 가격 변동 추이, 통계, 추천 아이템 및 잠재적 수익 정보를 확인할 수 있습니다.

## 주요 기능

### 1. 마비노기 경매장 데이터 수집 및 처리
- `adapter/mabinogi/mabinogi_client.py`: 마비노기 경매장으로부터 아이템 및 거래 내역 데이터를 수집합니다.
- `adapter/mabinogi/model/`: 수집된 데이터를 위한 `AuctionItemDto`, `AuctionHistoryDto`, `Item` 등의 데이터 모델을 정의합니다.
- `adapter/mabinogi/processor/`: 수집된 데이터를 필터링, 집계, 추출 및 정렬하는 다양한 처리 로직을 포함합니다. (예: `mabinogi_auction_item_filter.py`, `mabinogi_ohlc_extractor.py`)

### 2. 데이터 분석 및 추천 서비스
- `bot/service/recommend_service.py`: 사용자에게 유용한 아이템을 추천하는 로직을 구현합니다.
- `bot/revenue/calculate_revenue.py`: 특정 아이템의 잠재적 수익을 계산합니다.
- (이외의 서비스 파일들은 `src` 디렉토리가 확인되지 않아 제외되었습니다. 실제 프로젝트 구조에 따라 추가될 수 있습니다.)

### 3. 웹 인터페이스
- `templates/index.html`, `templates/chart.html`: 사용자 친화적인 웹 페이지를 제공합니다.
- `templates/style.css`, `templates/chart.html`: 웹 페이지의 스타일링을 담당합니다.
- (차트 관련 JavaScript 파일들은 `src/templates` 경로로 되어 있어 현재 프로젝트 구조에서는 제외되었습니다. 실제 프로젝트 구조에 따라 추가될 수 있습니다.)

### 4. Discord 봇 통합
- `bot/guild_client.py`: Discord 서버와 연동하여 봇 기능을 제공합니다.
- `bot/storage/`: 봇이 사용하는 아이템 목록 및 추천 아이템 목록을 저장합니다.


## 설치 및 실행 (예상)

1. **저장소 클론**:
   ```bash
   git clone https://github.com/jak010/tpjt-mabinogi-auction-src.git
   cd tpjt-mabinogi-auction-src
   ```

2. **의존성 설치**:
   ```bash
   pip install -r requirements.txt # requirements.txt 파일이 존재한다고 가정
   ```

3. **환경 변수 설정**:
   - 마비노기 API 키, Discord 봇 토큰 등 필요한 환경 변수를 설정합니다. (예: `.env` 파일 사용)

4. **애플리케이션 실행**:
   - 프로젝트의 메인 실행 파일 (예: `main.py` 또는 `app.py`)을 실행합니다. 정확한 실행 명령어는 프로젝트의 진입점에 따라 달라질 수 있습니다.

이후 웹 브라우저를 통해 웹 인터페이스에 접속하거나, Discord 봇을 초대하여 기능을 사용할 수 있습니다.
