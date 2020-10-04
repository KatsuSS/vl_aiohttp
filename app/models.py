from sqlalchemy import Column, Integer, String, Float, MetaData, Table, and_
import asyncpgsa


metadata = MetaData()

images = Table(
    "images", metadata,

    Column('image_id', Integer, primary_key=True),
    Column('account_id', Integer, nullable=False),
    Column('red', Float, nullable=False),
    Column('tag', String, nullable=True)
)


async def init_db(app):
    dsn = construct_db_url(app['config']['database'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app['db_pool'] = pool
    return pool


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )
    return DSN


async def get_count_by_params(conn, ac_id: int, tag: str, red_tg: float) -> int:
    """
    Подсчет количества изображений удовлетворяющих требованиям
    :param conn: подключение к DB
    :param ac_id: Id аккаунта создателя
    :param tag: его тег
    :param red_tg: минимальное количество красного
    :return: удовлетворяющее количество
    """
    query = images.select().where(and_(images.c.account_id == ac_id,
                                       images.c.tag == tag,
                                       images.c.red > red_tg))
    records = await conn.fetch(query)
    return len(records)


async def create_image(conn, account_id: int, amount_red: float, tag: str) -> int:
    """
    Создание нового изображения
    :param conn: подключение к DB
    :param account_id: Id аккаунта создателя
    :param amount_red: количество процентов пикселей с преобладанием красного
    :param tag: его тег
    :return: Id созданного изображения
    """
    stmt = images.insert().values(account_id=account_id, red=amount_red, tag=tag).returning(images.c.image_id)
    row = await conn.fetchrow(stmt)
    return row['image_id']


async def get_image_by_id(conn, im_id: int):
    """
    Получение картинки по Id
    :param conn: подключение к DB
    :param im_id: Id картинки в DB
    :return: строка поиска
    """
    result = await conn.fetchrow(
        images
        .select()
        .where(images.c.image_id == im_id)
    )
    return result


async def delete_image_by_id(conn, im_id: int):
    """
    Удаление картинки по его ID
    :param conn: подключение к DB
    :param im_id: Id картинки в DB
    :return: Id удаленного изображения или None
    """
    query = images.delete().where(images.c.image_id == im_id).returning(images.c.image_id)
    row = await conn.fetchrow(query)
    if row:
        return row.get('image_id', None)
    else:
        return None
