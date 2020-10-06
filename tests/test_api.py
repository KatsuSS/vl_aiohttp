async def test_new_images(tables, client):
    data = b'1234'
    params = {
        'account_id': 1,
        'tag': 'first'
    }
    response = await client.post('/images', params=params, data=data)
    assert response.status == 200
    data = await response.json()
    assert data == {'image_id': 1, 'red': 11.1, 'tag': 'first'}


async def test_get_image_info(client):
    response = await client.get('/images/1')
    assert response.status == 200
    data = await response.json()
    assert data == {'image_id': 1, 'account_id': 1, 'red': 11.1, 'tag': 'first'}


async def test_get__images_count(client):
    params = {'account_id': 1, 'red_tg': float(1.1), 'tag': 'first'}
    response = await client.get('/images/count', params=params)
    assert response.status == 200
    data = await response.text()
    assert data == "Number of satisfying images = 1"


async def test_del_image(client):
    response = await client.delete('/images/1')
    assert response.status == 200
    data = await response.text()
    assert data == "Image deleted with id = 1"


async def test_bad_request(client):
    params = {'ac_id': 1}
    response = await client.post('/images', params=params)
    assert response.status == 400
    params = {'account_id': 1, 'tag': 'first'}
    response = await client.get('/images/count', params=params)
    assert response.status == 400


async def test_not_found(client):
    response = await client.get('/')
    assert response.status == 404
    response = await client.get('/images/100')
    assert response.status == 404
    response = await client.get('/images/xxx')
    assert response.status == 404
