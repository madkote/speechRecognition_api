# /usr/bin/env python
# coding=utf-8

from aip import AipSpeech
from datetime import datetime
import wave
import subprocess
import os
import json
import sys
import base64
import contextlib
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
import time
import glob
import random
#import pandas as pd
# import seaborn
# seaborn.set(style='ticks')
# from IPython.display import Audio
import numpy as np
#import scipy
#import mir_eval
#import librosa
# from sklearn.externals import joblib
# import IPython.display
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import roc_curve,auc
# from sklearn.model_selection import StratifiedKFold

""" 你的 APPID AK SK """

APP_ID = '15414045'
API_KEY = 'BwSTqlxahGvI5k0kGIYDlybZ'
SECRET_KEY = 'g79fxW3Zqw1qrYKeQHmufv8zNXafc6Vt'

def num_aip(num):
    if num == 1:
        APP_ID = '15414045'
        API_KEY = 'BwSTqlxahGvI5k0kGIYDlybZ'
        SECRET_KEY = 'g79fxW3Zqw1qrYKeQHmufv8zNXafc6Vt'
    elif num == 2:
        APP_ID = '15546587'
        API_KEY = 'eFBR4VIUuDjfKm9rtBmhRiPD'
        SECRET_KEY = 'NW6kcX2GKRdFpuhNqMhL3kFIHutGV6IA'
    elif num == 3:
        APP_ID = '15511428'
        API_KEY = 'maQ5sigrenxv4HPSQBT6HMbk'
        SECRET_KEY = 'LPoWd9VrKFF9WW7LZnQvA3esW4G0r3Vw'
    elif num == 4:
        APP_ID = '15414045'
        API_KEY = 'BwSTqlxahGvI5k0kGIYDlybZ'
        SECRET_KEY = 'g79fxW3Zqw1qrYKeQHmufv8zNXafc6Vt'
    else:
        APP_ID = '15261457'
        API_KEY = 'R1QW860I09VloXydo7QMTdV7'
        SECRET_KEY = 'MIUjbU5KF96NqrSuoZ0LNNMhE5PPhwvs'
    return APP_ID, API_KEY, SECRET_KEY
class DemoError(Exception):
    pass
def fetch_token():
    num = random.randint(1, 5)
    APP_ID, API_KEY, SECRET_KEY = num_aip(num)
    TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

filename ='test0.wav'
with open(filename, 'rb') as speech_file:
        speech_data = speech_file.read()
token = fetch_token()
length = len(speech_data)
if length == 0:
    raise DemoError('file %s length read 0 bytes' % filename)
speech = base64.b64encode(speech_data)
speech = str(speech, 'utf-8')
params = {'dev_pid': 80001,
          'format': 'wav',
          'rate': 16000,
          'token': token,
          'cuid': '123456PYTHON',
          'channel': 1,
          'speech': speech,
          'len': length
          }
post_data = json.dumps(params, sort_keys=False)
# print post_data
ASR_URL = 'http://vop.baidu.com/pro_api'
req = Request(ASR_URL, post_data.encode('utf-8'))
req.add_header('Content-Type', 'application/json')
print(2, datetime.now())
try:
    f = urlopen(req)
    result_str = f.read()
except URLError as err:
    print('asr http response http code : ' + str(err.code))
    result_str = err.read()
print(2, datetime.now())
if len(result_str) != 0:
    data = str(result_str, 'utf-8')
    data = eval(data)
    print(data)
    if "err_no" in data:
        if data["err_no"] == 0:
            result = data["result"][0]
            status = "ok"
        elif data["err_no"] == 3301:
            message = "audio quality poor"  # equality error
        else:
            message = "other"  # other error
    else:
        message = "time out"
else:
    message = "500"