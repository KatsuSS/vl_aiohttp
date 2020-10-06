from aiohttp import web


async def handle_404(request):
    try:
        image_id = request.match_info['image_id']
    except Exception:
        image_id = None

    if image_id:
        return web.HTTPNotFound(text=f"Image with id={image_id} does not exist")
    else:
        return web.HTTPNotFound(text="This page Not Found")


async def handle_500(request):
    return web.HTTPInternalServerError(text="Internal Server Error")


async def handle_400(request, ex):
    return web.HTTPBadRequest(text=f"Bad parameters query: {ex.text}")


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response

        except web.HTTPBadRequest as ex:
            override = overrides.get(ex.status)
            return await override(request, ex)

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        400: handle_400,
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
