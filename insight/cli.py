# -*- coding: utf-8 -*-
import argparse

from .api import API

def sync(argv=None):
    parser = argparse.ArgumentParser(description='Sync InSight Raw Media Images')
    parser.add_argument('--overwrite', '-o', action='store_true', help='Re-download all')

    args, others = parser.parse_known_args(argv)    
    return API.sync(args.overwrite)