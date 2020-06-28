from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from myapp.speechrecognition import Recognition, zhRecognition, enRecognition, kuaizhRecognition
from datetime import datetime
import os
import json
import time
import glob

def hello(request):
    return HttpResponse('Hello World!')
class TestView(View):
    """类视图：处理注册"""
    def get(self, request):
        return HttpResponse('get Hello World!')
    def post(self, request):
        return HttpResponse('psot Hello World!')
class SpeechRecognitionView(View):
    # 判断中英文
    def post(self, request):
        language = request.POST.get('language', None) #语种
        audio_file = request.FILES.get('audio', None) #音频文件
        if not audio_file or not language or (language != 'zh' and language != 'en'):
            return HttpResponse({"upload audio or language error！"})
        filecontent = audio_file.read()
        filename = audio_file.name
        path_file_number = glob.glob(pathname='*.mp3')
        while len(path_file_number) >= 10:
            time.sleep(1)
            path_file_number = glob.glob(pathname='*.mp3')
        with open(filename, 'wb') as f:
            f.write(filecontent)
        response_data = Recognition(audio_file, language) #语音识别
        os.remove(filename)
        return HttpResponse(response_data)  # 返回json格式
class zhRecognitionView(View):
    # 中文识别
    def post(self, request):
        audio_file = request.FILES.get('audio', None)#音频文件
        # audio_file = eval(str(audio_file))
        # filecontent = audio_file.read()
        # audio_file = audio_file.name
        # print("audio_file.name:",audio_file.name)
        # print("audio_file.name type:",type(audio_file.name))
        # audio_file = str(audio_file)
        # if (audio_file.startswith('"') or audio_file.startswith("'") or audio_file.endswith('"') or audio_file.endswith("'")):
        #     audio_file = audio_file.replace('"','')
        #     audio_file = audio_file.replace("'",'')
        #     print(audio_file)
        #     print(type(audio_file))

        if not audio_file:
            return HttpResponse({"upload audio error！"})

        filecontent = audio_file.read()

        temp_time = str(time.time())
        audio_file_name = audio_file.name
        # filename = ''.join(audio_file.name)
        if (audio_file_name.startswith('"') or audio_file_name.startswith("'") or audio_file_name.endswith('"') or audio_file_name.endswith("'")):
            audio_file_name = audio_file_name.replace('"','')
            audio_file_name = audio_file_name.replace("'",'')
            # print(audio_file_name)
            # print(type(audio_file_name))
        filename = ''.join(audio_file_name)
        # filename = audio_file_name
        # print("filename:",filename)
        # print("filename type:",type(filename))
        filename = filename[:-4] + temp_time[-6:] + filename[-4:]
        # print("filename:",filename)
        # print("filename type:",type(filename))

        with open(filename, 'wb') as f:
            f.write(filecontent)
        # response_data = kuaizhRecognition(filename) #语音识别 加上性别年龄等
        response_data = zhRecognition(filename) #语音识别 普通版本的 
        os.remove(filename)
        return HttpResponse(response_data) # 返回json格式
class enRecognitionView(View):
    # 英文识别
    def post(self, request):
        audio_file = request.FILES.get('audio', None) #音频文件
        if not audio_file:
            return HttpResponse({"upload audio error！"})
        filecontent = audio_file.read()
        temp_time = str(time.time())
        filename = ''.join(audio_file.name)
        filename = filename[:-4] + temp_time[-6:] + filename[-4:]
        with open(filename, 'wb') as f:
            f.write(filecontent)
        response_data = enRecognition(filename) #语音识别
        os.remove(filename)
        return HttpResponse(response_data)  # 返回json格式
if __name__ == '__main__':
    path_file_number = glob.glob(pathname='*.mp3')
    print(path_file_number)
    res = SpeechRecognitionView()
    print(res)