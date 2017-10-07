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
import sha3

# define constant values
# URL of Bing Search API
API_URL = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'

# timeout for downloading image. (sec)
TIMEOUT = 5

# Max number of images to collect defined by Bing Image Search API v5.0.
IMAGES_PER_REQUEST = 10

# This func returns path to collected images folder.
def get_image_folder():
    path_to_current_directory = os.path.dirname( os.path.abspath(__file__))
    path_to_image_directory = path_to_current_directory + '/media/'

    # If directory don't exists, make directory.
    if not os.path.isdir(path_to_image_directory):
        os.mkdir(path_to_image_directory)
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

# make path to save image at
def make_image_path(dirpath, url):
    file_extension = os.path.splitext(url)[-1]
    
    if file_extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
        # required encoding for hashed
        encoded_url = url.encode('utf-8')
        hashed_url = str(hashlib.sha3_256(encoded_url).hexdigest())
        file_name = hashed_url.replace('\'', '')
        full_path = os.path.join(dirpath, hashed_url + hashed_url)

        return full_path

    else:
        raise ValueError('not applicable file extension')


def download_image(url):
    response = requests.get(url, allow_redirects=True, timeout=TIMEOUT)
    if response.status_code != 200:
        error = Exception("HTTP status: " + response.status_code)
        raise error
    
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        error = Exception('Content-Type : ' + content_type)
        raise error
    
    return response.content

def save_image(filepath, image):
    with open(filepath, "wb") as fout:
        fout.write(image)

# request with header and params
def request_images_and_save(header, params):
    url_list = []

    try:
        # connection = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        # connection.request("POST", "/bing/v5.0/images/search?%s" % params, "{body}", header)
        # response = connection.getresponse()
        # data = response.read()

        res = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/images/search', headers=header, params=params)

        # connection.close()
    except:
        raise Exception('connecting failed')
    else:
        # decoded_response = data.decode('utf-8')
        data = res.json()
        
        pattern = r"&r=(http.+)&p="

        for values in data['value']:
            unquoted_url = urllib.parse.unquote(values['contentUrl'])
            image_url = re.search(pattern, unquoted_url)

            if image_url:
                url_list.append(image_url.group(1))
    
    for url in url_list:
        try:
            print(url)
            image_path = make_image_path(get_image_folder(), url)
            print(image_path)
            image = download_image(url)
            save_image(image_path, image)
        except Exception as err:
            print("%s" % (err))
            continue

        return


# If this file is executed from commandline, below script will execute.
if __name__ == '__main__':
    # parse command line arguments
    args = parse_arguments()

    # make request header
    header = make_request_header(args.API_key)

    for i in range(args.num_of_image // IMAGES_PER_REQUEST):

        # offset is the number of images to skip before returning images
        offset = i * IMAGES_PER_REQUEST
        
        # make request params
        params = make_request_params(args.query, offset)
        
        request_images_and_save(header, params)
        

        
    



    