from app.main import create_app
from aiohttp import web


app = create_app()
web.run_app(app, host='127.0.0.1', port=8080)
