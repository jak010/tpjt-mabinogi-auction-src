from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from src.controller.markets import markets_router


class MabinogiAuctionTrackingApplication:

    def __init__(self) -> None:
        self.app = FastAPI(
            title="Mabinogi Auction Tracking API",
            description="Mabinogi Auction Tracking API",
            version="1.0.0"
        )
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    def __call__(self):
        self.app.include_router(markets_router)

        # Serve static files (CSS, JS, etc.) from the templates directory
        self.app.mount("/static", StaticFiles(directory=self.templates_dir), name="static")

        @self.app.get("/")
        async def read_root():
            return FileResponse(os.path.join(self.templates_dir, "index.html"))

        @self.app.get("/chart")
        async def read_chart():
            return FileResponse(os.path.join(self.templates_dir, "chart.html"))

        return self.app


# uvicorn src.main:application --relaoad
application = MabinogiAuctionTrackingApplication()
