import yaml
import numpy as np
from matplotlib.image import imread
import cv2
from aiohttp.web_request import Request


def load_config(config: str) -> dict:
    """
    Загрузка конфига из yaml файла
    :param config: yaml файл конфига
    :return: dict config
    """
    with open(config, 'r') as stream:
        try:
            conf_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf_data


async def get_image(request: Request):
    """
    Преобразует байты из буфера в картинку
    :param request:
    :return:
    """
    np_image_bytes = np.frombuffer(await request.content.read(), np.uint8)
    np_image = cv2.imdecode(np_image_bytes, -1)
    return np_image


def get_amount_of_red(np_image) -> float:
    """
    Считает процент пикселей, где преобладает красный свет
    :param np_image: картинка
    :return: процент преобладающих пикселей
    """
    im_array = imread(np_image).reshape(-1, 3)
    temp = (im_array[:, 0] > im_array[:, 1]) & (im_array[:, 0] > im_array[:, 2])
    return np.count_nonzero(temp) / len(temp) * 100
