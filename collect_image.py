# -*- coding: utf-8 -*-

'''
    This file is test for using "Bing Search APIs".
    Its goal is collecting images from web.
'''

import http.client
import json
import re
import requests
import os
import math
import pickle
import urllib
import hashlib
import argparse
# import sha3

# define constant values
# URL of Bing Search API
API_URL = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'

# timeout for downloading image. (sec)
TIMEOUT = 5

# Max number of images to collect defined by Bing Image Search API v5.0.
IMAGES_PER_REQUEST = 50

# This func returns path to collected images folder.
def get_image_folder():
    path_to_current_directory = os.path.dirname( os.path.abspath(__file__))
    path_to_image_directory = path_to_current_directory + '/media/'
    return path_to_image_directory

# This func parse commandline arguments.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect images by Bing Image Search API')
    parser.add_argument('API_key', type=str, help='API_key for Bing Search API')
    parser.add_argument('num_of_image', type=int, help='number of images to collect')
    parser.add_argument('query', type=str, help='search word')
    args = parser.parse_args()

    # if args.num_of_image % IMAGES_PER_REQUEST != 0:
    #     raise Exception('number must be divisible by {0}'.format(IMAGES_PER_REQUEST))

    return args

def make_request_header(API_key):
    header = {
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': API_key,
    }
    return header

def make_request_params(query, offset):
    params = urllib.parse.urlencode({
        'q': query,
        'mkt': 'ja-JP',
        'count': IMAGES_PER_REQUEST,
        'offset': offset
    })
    return params


# If this file is executed from commandline, below script will execute.
if __name__ == '__main__':
    # parse command line arguments
    args = parse_arguments()

    # make request header
    header = make_request_header(args.API_key)

    for i in range(args.count // IMAGES_PER_REQUEST):

        # offset is the number of images to skip before returning images
        offset = i * IMAGES_PER_REQUEST
        # make request params
        params = make_request_params(args.query, offset)

        
    



    