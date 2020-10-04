from app.views import images, get_images_count, get_image_inf, del_image
from aiohttp.web_app import Application


def setup_routes(app: Application):
    app.router.add_post('/images', images, name="images")
    app.router.add_get('/images/count', get_images_count, name="get_images_count")
    app.router.add_get('/images/{image_id:\d+}', get_image_inf, name="get_image_inf")
    app.router.add_delete('/images/{image_id:\d+}', del_image, name="del_image")
