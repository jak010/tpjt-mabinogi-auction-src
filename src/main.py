from fastapi import FastAPI

from src.controller.markets import markets_router


class MabinogiAuctionTrackingApplication:

    def __init__(self) -> None:
        self.app = FastAPI(
            title="Mabinogi Auction Tracking API",
            description="Mabinogi Auction Tracking API",
            version="1.0.0"
        )

    def __call__(self):
        self.app.include_router(markets_router)

        return self.app


# uvicorn src.main:application --relaoad
application = MabinogiAuctionTrackingApplication()
