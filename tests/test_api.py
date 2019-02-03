# -*- coding: utf-8 -*-
import pytest
import requests_mock
import os

from insight import API

from insight.image import Image

@pytest.fixture
def response():
    return {'items': [{'id': 11,
                       'camera_vector': '',
                       'site': None,
                       'imageid': 'C000M0000_596533559EDR_F0000_0106M_',
                       'subframe_rect': '(1,1,1024,1024)',
                       'sol': 0,
                       'scale_factor': 1,
                       'camera_model_component_list': '',
                       'instrument': 'icc',
                       'url': 'https://mars.nasa.gov/insight-raw-images/surface/sol/0000/icc/C000M0000_596533559EDR_F0000_0106M_.PNG',
                       'spacecraft_clock': 596533559.23421,
                       'attitude': '',
                       'camera_position': '',
                       'camera_model_type': '',
                       'drive': None,
                       'xyz': '',
                       'created_at': '2018-11-27T02:40:07.637Z',
                       'updated_at': '2018-11-27T02:47:15.551Z',
                       'mission': 'insight',
                       'extended': '{"localtime": "13:34:21"}',
                       'date_taken': '2018-11-26T00:00:00.000Z',
                       'date_received': '2018-11-26T00:00:00.000Z',
                       'instrument_sort': 99,
                       'sample_type_sort': 99,
                       'is_thumbnail': False,
                       'title': 'Sol 0: Instrument Context Camera (ICC)',
                       'description': "NASA's InSight Mars lander acquired this image of the area in front of the lander using its lander-mounted, Instrument Context Camera (ICC).<br /><br />This image was acquired on November 26, 2018, Sol 0 of the InSight mission where the local mean solar time for the image exposures was 13:34:21 PM. Each ICC image has a field of view of 124 x 124 degrees."}],
            'more': True,
            'total': 2,
            'page': 0,
            'per_page': 1}

def test_api_url():
    assert API.api == 'https://mars.nasa.gov/api/v1/raw_image_items'
    
def test_api_count_imgs():
    assert API.count_imgs() > 0

def test_api_get_imgs():
    img = API.get_imgs(limit=1, order=['date_taken+asc'])[0]
    assert isinstance(img, Image)
    assert str(img) == img.json['imageid']

    img.download()
    assert os.path.exists(img.imageid + '.PNG')
    os.remove(img.imageid + '.PNG')

def test_api_sync(requests_mock, response):
    img = response['items'][0]
    requests_mock.get(API.api + '/?order=date_taken+asc&per_page=500&page=0', json=response)
    requests_mock.get(API.api + '/?order=date_taken+asc&per_page=500&page=1', json=response)
    requests_mock.get(img['url'], real_http=True)
    
    API.sync(folder='tests')
    png = os.path.join('tests', img['instrument'].upper(), f"{img['sol']:04d}", img['imageid'] + '.PNG')
    assert os.path.exists(png)

    # Clean `tests` folder
    os.remove(os.path.join('tests', img['instrument'].upper(), f"{img['sol']:04d}", img['imageid'] + '.PNG'))
    os.removedirs(os.path.join('tests', img['instrument'].upper(), f"{img['sol']:04d}"))

