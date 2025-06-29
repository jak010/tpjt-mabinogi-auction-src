import os

from fastapi import FastAPI

from src.controller.markets import markets_router

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Mabinogi Auction Tracking API",
    description="Mabinogi Auction Tracking API",
    version="1.0.0"
)

# 템플릿 디렉토리 설정
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

# 라우터 포함
app.include_router(markets_router)

# uvicorn이 참조할 ASGI 애플리케이션
application = app
