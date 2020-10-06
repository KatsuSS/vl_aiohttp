import pytest
from app.main import create_app
from settings import BASE_DIR
from app.utils import load_config
from db import setup_db, teardown_db, create_tables, drop_tables


@pytest.fixture(scope='session')
def database():
    db_config = load_config(f'{BASE_DIR}/config_test.yaml')['database_postgres']
    setup_db(config=db_config)
    yield
    teardown_db(config=db_config)


@pytest.fixture(scope='session')
def tables(database):
    db_config = load_config(f'{BASE_DIR}/config_test.yaml')['database_test']
    create_tables(config=db_config)
    yield
    drop_tables(config=db_config)


@pytest.fixture
async def client(aiohttp_client):
    config = f'{BASE_DIR}/config_test.yaml'
    app = await create_app(config)
    return await aiohttp_client(app)
