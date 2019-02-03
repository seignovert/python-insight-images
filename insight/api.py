# -*- coding: utf-8 -*-
import os
import requests
from tqdm import tqdm

from .image import Image

API_URL = 'https://mars.nasa.gov'
VERSION = 'v1'

class Api(object):
    '''
    Insight raw media images API

    Parameters
    ----------
    url: str, optional
        API root url.
    version: str, optional
        API version
    '''

    def __init__(self, url=API_URL, version=VERSION):
        self.url = url
        self.version = version
        self.api = self.url + '/api/' + self.version + '/raw_image_items'

    def get(self, url):
        '''
        GET request on the API

        Parameters
        ----------
        url: str
            GET url reaquested

        Return
        ------
        dict:
            Parsed JSON API response

        Raises
        ------
        requests.reponse.HTMLError
            If HTML error is thrown by the API (HTML code not equal 200)
        '''
        resp = requests.get(self.api + url)
        assert resp.ok, resp.raise_for_status()
        return resp.json()

    @property
    def latest(self):
        '''
        Request the latest images from the API

        Return
        ------
        dict:
            List of the latest data

        Raises
        ------
        IOError
            Thown on API reauest failed
        '''
        json = self.get('/insight/latest')
        assert json['success'], f"API latest query failed:\n{json}"

        return json['latest_data']

    def count_imgs(self):
        '''
        Count the total number of images available

        Return
        ------
        int
            Number of available images since the latest release.
        '''
        return self.latest['total']

    def get_page(self, url, page):
        '''
        Request for a specific page

        Parameters
        ----------
        url: str
            Query url
        page: int
            Page to query

        Return
        ------
        dict
            API JSON result for the requested page
        '''
        return self.get(url + '&page=' + str(page))

    def get_all_pages(self, url):
        '''
        Loop other all the available pages

        Parameters
        ----------
        url: str
            Query url

        Return
        ------
        [dict]
            Array of all items from API JSON response
        '''
        json = self.get_page(url, 0)
        data = json['items']
        nb_pages = int((json['total']-1)/json['per_page']) + 1
        for page in range(1, nb_pages):
            data += self.get_page(url, page)['items']
        return data

    def get_imgs(self, limit=None, order=['sol+desc','date_taken+desc'], per_page=500):
        '''
        Queries the list of images

        Parameters
        ----------
        limit: int, optional
            Restrict the number of images output (requested in a single query).
        order: [str], optional
            Images order key names with ``+desc`` or ``+asc`` ordering

        Other Parameters
        ----------------
        per_page: int, optional
            Maximum number for result per page request. Disable is ``limit`` is not ``None``.

        Return
        ------
        [insight.Image]
            List of InSight images
        '''
        url = '/?order=' + '%2C'.join(order)

        if limit is None:
            url += '&per_page=' + str(per_page)
            imgs = self.get_all_pages(url)
        else:
            url += '&per_page=' + str(limit)
            imgs = self.get_page(url, 0)['items']

        return [Image(json) for json in imgs]

    def sync(self, folder=None, overwrite=False):
        '''
        Sync output all the image inside output folder

        Parameters
        ----------
        folder: str, optional
            Output folder to sync
        overwrite: bool, optional
            Overwrite all images
        '''
        root = os.getcwd() if not folder else folder
        
        for img in tqdm(self.get_imgs(order=['date_taken+asc'])):
            assert 'instrument' in img, f'Argument `instrument` is missing in `{img}`'
            assert 'sol' in img, f'Argument `sol` is missing in `{img}`'

            fout = os.path.join(root, img.instrument.upper(), f'{img.sol:04d}')
            if not os.path.isdir(fout):
                os.makedirs(fout)

            fout = os.path.join(fout, img.imageid + '.PNG')
            
            try:
                img.download(fout, overwrite=overwrite, verbose=False)
            except FileExistsError:
                pass


# Default API interface
API = Api()
