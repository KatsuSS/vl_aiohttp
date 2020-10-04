from aiohttp import web
from app.utils import get_amount_of_red, get_image
from app import models as db
from aiohttp.web_request import Request


async def images(request):
    """
    Добавление нового изображения с параметрами
    :param request:
        - account_id: id аакаунта отправителя
        - tag: тег отправителя, если есть
        - байт код изображения
    :return:
    """
    try:
        account_id = int(request.rel_url.query['account_id'])
    except KeyError as e:
        return web.Response(text=f"Need all parameters query: {e}")
    tag = request.rel_url.query.get('tag', None)

    image = await get_image(request)
    amount_red = get_amount_of_red(image)
    async with request.app['db_pool'].acquire() as conn:
        image_id = await db.create_image(conn, account_id, amount_red, tag)
    return web.json_response({'image_id': image_id, 'red': amount_red, 'tag': tag})


async def get_image_inf(request):
    """
    Вывод информации об изображении по его Id
    :param request:
        - image_id: Id изображения в БД
    :return: {image_id:, account_id:, rea:, tag:}
    """
    image_id = request.match_info['image_id']
    async with request.app['db_pool'].acquire() as conn:
        res = await db.get_image_by_id(conn, int(image_id))
    if res:
        return web.json_response({'image_id': res['image_id'], 'account_id': res['account_id'],
                                  'red': float(res['red']), 'tag': res['tag']})
    else:
        return web.Response(text=f"Image with id={image_id} does not exist")


async def del_image(request):
    """
    Удаление изображения по его Id
    :param request:
        - image_id: Id изображения в БД
    :return: возвращает Id удаленного изображения
    """
    image_id = request.match_info['image_id']
    async with request.app['db_pool'].acquire() as conn:
        im_id = await db.delete_image_by_id(conn, int(image_id))
    if im_id:
        return web.Response(text=f"Image deleted with id = {im_id}")
    else:
        return web.Response(text=f"No picture in DB with id = {image_id}")


async def get_images_count(request):
    """
    Поиск количества записей картинок, удовлетворяющих параметрам
    :param request:
        - account_id: id аакаунта отправителя
        - tag: тег отправителя, если есть
        - минимальное количество красного
    :return: count:int - количество совпадений
    """
    params = request.rel_url.query
    try:
        ac_id, tag, red_tg = int(params['account_id']), params['tag'], params['red_tg']
    except KeyError as e:
        return web.Response(text=f"Need all parameters query: {e}")

    async with request.app['db_pool'].acquire() as conn:
        count = await db.get_count_by_params(conn, ac_id, tag, red_tg)
    return web.Response(text=f"Number of satisfying images = {count}")
