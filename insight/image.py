# -*- coding: utf-8 -*-
import os
import requests
from tqdm import tqdm

class Image(object):
    '''
    Insight raw media image

    Parameters
    ----------
    json: dict
        API Image JSON response

    Other Parameters
    ----------------
    name: str
        Image ID
    '''

    def __init__(self, json=None, **kwargs):
        if json:
            self.json = json
        else:
            self.json = kwargs
    
    def __str__(self):
        assert 'imageid' in self, 'Attribute `imageid` missing'
        return self.imageid

    def __repr__(self):
        return f'<InSight Image> {str(self)}'

    def __contains__(self, item):
        return item in self.__dict__.keys()

    @property
    def json(self):
        return self.__json
    
    @json.setter
    def json(self, json):
        self.__json = json
        for key, value in json.items():
            if value is not None or value != '':
                setattr(self, key, value)    

    def download(self, out=None, overwrite=False, verbose=True):
        '''
        Download image url

        Parameters
        ----------
        out: str, optional
            Output filename
        overwrite: bool, optional
            If exists, overwrite output file
        verbose: bool, optional
            Add download progress bar
        '''
        assert 'url' in self, 'Keyword missing: `url`'

        if not out:
            out = self.url.split('/')[-1]
        else:
            assert out.lower().endswith('.png'), 'Output filename must ends with `.png`'

        if os.path.exists(out) and not overwrite:
            raise FileExistsError(f'File `{out}` exists')

        resp = requests.get(self.url, allow_redirects=True, stream=True)

        if resp.status_code == 200:
            with open(out + '_tmp', 'wb') as f:
                if verbose:
                    for chunk in tqdm(resp.iter_content(1024), desc=f"Download {out}", unit=' kB'):
                        f.write(chunk)
                    print('')
                else:
                    for chunk in resp:
                        f.write(chunk)
            os.rename(out + '_tmp', out)

