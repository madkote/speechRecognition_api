from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from videototextapp.videototext import video_to_text
import time
import json
import os
from datetime import datetime
# Create your views here.

def videototexthello(request):
    return HttpResponse('Hello World, videototext !')

class bandwidthView(View):
    def post(self, request):
        start = datetime.now()
        video_file = request.FILES.get('video', None)
        if not video_file:
            return HttpResponse({"upload video error！"})
        filecontent = video_file.read()
        filename = ''.join(video_file.name)
        temp_time = str(time.time())
        filename = filename[:-4] + temp_time[-6:] + filename[-4:]
        with open(filename, 'wb') as f:
            f.write(filecontent)
        try:
            f = open(filename)
            f.close()
        except IOError:
            print('no file')
        end = datetime.now()
        print('upload_time:', end-start)
        upload_time ={'upload_time': 0}
        upload_time['upload_time'] = str(end-start)
        os.remove(filename)
        return HttpResponse(json.dumps(upload_time))  # 返回json格式

class videototextView(View):
    def post(self, request):
        start = datetime.now()
        language = request.POST.get('language', None)
        video_file = request.FILES.get('video', None)
        if not video_file or not language or (language != 'zh' and language != 'en'):
            return HttpResponse({"upload video or language error！"})
        filecontent = video_file.read()
        temp_time = str(time.time())
        filename = ''.join(video_file.name)
        filename = filename[:-4] + temp_time[-6:] + filename[-4:]
        print('filename:', filename)
        with open(filename, 'wb') as f:
            f.write(filecontent)
        try:
            f = open(filename)
            f.close()
        except IOError:
            print('no file')
        upload_time = datetime.now()
        print('upload_time:',upload_time - start)
        response_data = video_to_text(language, filename)  # 语音识别
        os.remove(filename)
        recognition_time = datetime.now()
        response_data["upload_time"] = str(upload_time - start)
        response_data["recognition_time"] = str(recognition_time - upload_time)
        response_data = json.dumps(response_data, ensure_ascii=False)
        return HttpResponse(response_data)  # 返回json格式
