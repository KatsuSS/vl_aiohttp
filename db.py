from sqlalchemy import create_engine, MetaData

from app.models import construct_db_url
from app.models import images
from app.utils import load_config


def setup_db(config=None):
    engine = get_engine(config)
    db_name = config['DB_NAME_TEST']

    with engine.connect() as conn:
        teardown_db(config=config)
        conn.execute("CREATE DATABASE %s" % db_name)


def teardown_db(config=None):
    engine = get_engine(config)
    db_name = config['DB_NAME_TEST']

    with engine.connect() as conn:
        # terminate all connections to be able to drop database
        conn.execute("SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity "
                     "WHERE pg_stat_activity.datname = '%s' AND pid <> pg_backend_pid();" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)


def get_engine(db_config):
    db_url = construct_db_url(db_config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


def create_tables(config=None):
    engine = get_engine(config)

    meta = MetaData()
    meta.create_all(bind=engine, tables=[images])


def drop_tables(config=None):
    engine = get_engine(config)

    meta = MetaData()
    meta.drop_all(bind=engine, tables=[images])


def create_sample_data(config=None):
    engine = get_engine(config)

    with engine.connect() as conn:
        conn.execute(images.insert(), [
            {'account_id': 1,
             'red': 73.3,
             'tag': 'first'},
            {'account_id': 2,
             'red': 13,
             'tag': 'second'},
        ])


if __name__ == '__main__':
    db_config_postgres = load_config('config.yaml')['database_postgres']
    db_config_test = load_config('config.yaml')['database_test']

    teardown_db(config=db_config_postgres)
    setup_db(config=db_config_postgres)
    create_tables(config=db_config_test)
    create_sample_data(config=db_config_test)
