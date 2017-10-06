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
# import sha3

# This func returns path to collected images folder.
def get_image_folder():
    path_to_current_directory = os.path.dirname( os.path.abspath(__file__))
    path_to_image_directory = path_to_current_directory + '/media/'
    return path_to_image_directory

# If this file is executed from commandline, below script will execute.
if __name__ == '__main__':
    print(get_image_folder())