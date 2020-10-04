from aiohttp import web
from app.routes import setup_routes
from app.models import init_db
from app.utils import load_config
from aiohttp.web_app import Application


async def create_app(config: str = "config.yaml") -> Application:
    config = load_config(config)
    app = web.Application()
    setup_routes(app)
    app['config'] = config
    await init_db(app)

    return app
