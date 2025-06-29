import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .controller.markets import markets_router

class ApplicationBuilder:
    def __init__(self):
        self.app = FastAPI(
            title="Mabinogi Auction Tracking API",
            description="Mabinogi Auction Tracking API",
            version="1.0.0"
        )
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.templates = Jinja2Templates(directory=self.templates_dir)

    def _configure_static_files(self):
        self.app.mount("/static", StaticFiles(directory=self.templates_dir), name="static")

    def _include_routers(self):
        self.app.include_router(markets_router)

    def _add_routes(self):
        @self.app.get("/")
        async def index(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

    def build_app(self) -> FastAPI:
        self._configure_static_files()
        self._include_routers()
        self._add_routes()
        return self.app

application = ApplicationBuilder().build_app()
