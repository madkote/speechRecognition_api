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
from sklearn.externals import joblib
import librosa
import numpy as np
from myapp.utils1 import load_model, Predict
import threading
""" 你的 APPID AK SK """
APP_ID = '15414045'
API_KEY = 'BwSTqlxahGvI5k0kGIYDlybZ'
SECRET_KEY = 'g79fxW3Zqw1qrYKeQHmufv8zNXafc6Vt'

model_name ='mlp_librosa'
model = load_model(model_name)
clffa = joblib.load('myapp/cfl_age.pkl')#年龄识别
clffg = joblib.load('myapp/gender.joblib')#性别识别
def feature(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    stft = np.abs(librosa.stft(y))
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T,axis=0)
    features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    features = features.reshape(1, -1)
    return features
def genderageRecognition(filename,gender,age):
    features = feature(filename)
    genders = clffg.predict(features)
    if genders[0]==1:
        gender.append('男')
    else:
        gender.append('女')
    ages = clffa.predict(features)
    if ages[0]=='Youth':
        age.append('青少年')
    elif ages[0]=='Senior':
        age.append('老人')
    else:
        age.append('成年人')
    #return gender, age
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
def Audiotime(filename):
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames/float(rate)
    return duration

def Recognition(audio_file, language):
    # 判断中英文
    start = datetime.now()
    #filename = ''.join(audio_file.name)
    # temp_time = str(time.time())
    # duration = Audiotime(audio_file)  # 判断音频时长
    # print(duration)
    # if duration > 15:
    #     message = "1"  # time too long
    #     response_data = json.dumps({"status": status, "message": message, "result": result})
    #     return response_data
    aip = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    if language == 'zh':
        num = 1537
    else:
        num = 1737
    filename = ''.join(audio_file.name)
    temp_time = str(time.time())
    filename = filename[:-4] + temp_time[-6:] + '.wav'
    command = 'ffmpeg -y -i %s %s' % (audio_file, filename)
    subprocess.call(command, shell=True)
    with open(filename, 'rb') as f:
        file_content = f.read()
    data = aip.asr(file_content, 'wav', 16000, {
        'dev_pid': num,
    })
    end = datetime.now()
    os.remove(filename)
    print(data)
    print('used time is : ', end - start)
    if data['err_no'] == 0:
        result = data['result'][0]
        status = "ok"
        message = "0"
        response_data = json.dumps({"status": status, "message": message,"result": result})
        return response_data  # 返回json格式
    else:
        status = "error"
        message = "1"
        result = ""
        response_data = json.dumps({"status": status, "message": message,"result": result})

        return response_data

def zhRecognition(audio_file):
    # 判断中英文
    start = datetime.now()
    status = "error"
    message = "right"
    result = ""
    format = False
    filename = audio_file
    path_file_number = glob.glob(pathname='*.wav')
    while len(path_file_number) >= 10:
        time.sleep(1)
        path_file_number = glob.glob(pathname='*.wav')
    if audio_file[-3:] != 'wav':
        filename = audio_file[:-4] + '.wav'
        command = 'ffmpeg -y -i %s %s' % (audio_file, filename)
        subprocess.call(command, shell=True)
        format = True
    try:
        with open(filename, 'rb') as f:
            file_content = f.read()
        aip = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        data = aip.asr(file_content, 'wav', 16000, {
            'dev_pid': 1536,
        })
        end = datetime.now()
        print(data)
        print('used time is : ', end - start)
        if "err_no" in data:
            if data['err_no'] == 0:
                result = data['result'][0]
                status = "ok"
            elif data["err_no"] == 3301:
                message = "audio quality poor"
            else:
                message = "other"
        else:
            message = "time out"
        response_data = json.dumps({"status": status, "message": message, "result": result})
        if format:
            os.remove(filename)
        return response_data
    except :
        response_data = json.dumps({"status": "error", "message": "Please check the file naming format", "result": ""})
        return response_data


def enRecognition(audio_file):
    start = datetime.now()
    #随机产生整数，调用不同账号
    num = random.randint(1, 5)
    APP_ID, API_KEY, SECRET_KEY = num_aip(num)
    aip = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    status = "error"
    message = "right"
    result = ""
    format = False
    filename = audio_file
    if audio_file[-3:] != 'wav':
        filename = audio_file[:-4] + '.wav'
        command = 'ffmpeg -y -i %s %s' % (audio_file, filename)
        subprocess.call(command, shell=True)
        format = True
    with open(filename, 'rb') as f:
        file_content = f.read()
    if format:
        os.remove(filename)
    data = aip.asr(file_content, 'wav', 16000, {
        'dev_pid': 1737,
    })
    #os.remove(audio_file)
    end = datetime.now()
    print(data)
    print('used time is : ', end - start)
    if "err_no" in data:
        if data['err_no'] == 0:
            result = data['result'][0]
            status = "ok"
        elif data["err_no"] == 3301:
            message = "audio quality poor"
        else:
            message = "other"
    else:
        message = "time out"
    response_data = json.dumps({"status": status, "message": message, "result": result})
    return response_data

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

def speechRecognition(filename,status,message,results):
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
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
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
    results.append(result)
    results.append(status)
    results.append(message)
    #return result,status,message
    
def kuaizhRecognition(audio_file):
    start = datetime.now()
    token = fetch_token()
    status = "error"
    message = "right"
    result = ""
    gender = []
    age = []
    emotion = []
    results = []
    # duration = Audiotime(audio_file)  # 判断音频时长
    # if duration > 15:
    #     message = "1"  # time too long
    #     response_data = json.dumps({"status": status, "message": message, "result": result})
    #     return response_data
    format = False
    filename = audio_file
    if filename[-3:] != 'wav':
        format = True
        filename = audio_file[:-4] + '.wav'
        command = 'ffmpeg -y -i %s -ar 16000 %s' % (audio_file, filename)
        subprocess.call(command, shell=True)
    # time1 = datetime.now()
    # gender, age = genderageRecognition(filename)
    # time2 = datetime.now()
    # emotion = Predict(model, model_name, filename)
    # time3 = datetime.now()
    # result, status, message = speechRecognition(filename, status, message)
    # time4 = datetime.now()
    #time1 = datetime.now()
    # t1 = threading.Thread(target=genderageRecognition(filename, gender, age))
    # t2 = threading.Thread(target=Predict(model, model_name, filename, emotion))
    # t3 = threading.Thread(target=speechRecognition(filename, status, message, results))
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()
    time1 = datetime.now()
    genderageRecognition(filename, gender, age)
    time2 = datetime.now()
    Predict(model, model_name, filename, emotion)
    time3 = datetime.now()
    speechRecognition(filename, status, message, results)
    time4 = datetime.now()
    genderage = "(" + gender[-1] + "/" + age[-1] + "/" + emotion[-1] + ")"
    result, status, message = results[0], results[1], results[2]
    result = genderage + result
    print(result)
    if format:
        os.remove(filename)
    end = datetime.now()
    print('genderage_time: ',time2-time1)
    print('emotion_time: ', time3 - time2)
    print('speech_time: ', time4 - time3)
    print('used time is : ', end - start)
    response_data = json.dumps({"status": status, "message": message, "result": result})
    return response_data

if __name__ == '__main__':
    audio_file = '1.mp3'
    res = enRecognition(audio_file)
    print(res)
