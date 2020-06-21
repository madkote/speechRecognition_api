from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import time
from .tasks import *
import os
import json
# from videoaddsubtitleapp.enzh_videoaddtitle import subtitle
from videoaddsubtitleapp.tasks import subtitle
import subprocess
# Create your views here.
from celery.result import AsyncResult
def videohello(request):
    return HttpResponse('Hello World! videoaddsubtitle')
class runstate(View):
    def post (self,request):
        task_id = request.POST.get('id', None)
        result = AsyncResult(task_id)
        print(result.state)
        if result.state =='SUCCESS':
            data = result.result
        else:
            data = json.dumps({"status": 'pending', "message": 'pleace wait ...', "result": ""})
        print(data)
        return HttpResponse(data)
class videoaddsubtitle(View):
    # 英文识别
    def post(self, request):
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
        response_data = subtitle.delay(language, filename) #语音识别
        print(response_data)
        return HttpResponse(response_data)  # 返回json格式
