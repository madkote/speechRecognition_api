import subprocess
import sys
import os
from datetime import datetime
import argparse
import random
import hashlib
import urllib.request
import http.client
import json
import time
import threading
from threading import Thread, current_thread
import queue



parser = argparse.ArgumentParser()
parser.add_argument('--language', default='en', type=str, help='recognition type zh,zhen or en,enzh')
parser.add_argument('--subtitle', default=2, type=int, help='subtitle num 1 or 2')
parser.add_argument('--interval', default=250, type=int, help='interval time ms')
parser.add_argument('--data-input', default='data_input', type=str, help='data input')
parser.add_argument('--data-out', default='data_out', type=str, help='data out')
args = parser.parse_args()

def video_srt(params=None):
    # 视频添加字幕
    path_input = params['path_input']
    path_srt = params['srt']
    file_srt = "subtitles=%s" % (path_srt)
    path_out = params['path_out']
    command = 'ffmpeg -y -i %s -vf %s -strict -2 %s' % (path_input, file_srt, path_out)  # -shortest
    subprocess.call(command, shell=True)


if __name__=='__main__':
    data_input = args.data_input
    if os.path.isdir(data_input):
        list_input = os.listdir(data_input)
    else:
        data_input, filename = os.path.split(data_input)
        list_input = [filename]
    data_out = args.data_out
    start_time = datetime.now()
    for i in range(0, len(list_input)):
        if list_input[i][-3:] == r'mp4' or list_input[i][-3:] == r'mkv' or list_input[i][-3:] == r'MOV':
            path_input = os.path.join(data_input, list_input[i])
            file_name = os.path.splitext(list_input[i])[0:-1]
            data_out = sys.path[0] + '/data_out/' + "".join(tuple(file_name)) + '/'
            os.makedirs(data_out, exist_ok=True)

            # 添加字幕，多线程
            path_srt = data_out + '%s.srt'%(file_name)  # source srt
            enzh_srt = data_out + 'enzh%s.srt' % (file_name)  # translate
            path_out = os.path.join(data_out, list_input[i])
            enzh_out = os.path.join(data_out, 'enzh'+ list_input[i])
            t1 = threading.Thread(target=video_srt,
                                  kwargs={'params': {'path_input': path_input, 'srt': path_srt,
                                                     'path_out': path_out}})  # 创建一个线程对象t1 子线程
            thread1 = []
            thread1.append(t1)
            if args.subtitle == 2:
                t2 = threading.Thread(target=video_srt,
                                      kwargs={'params': {'path_input': path_input, 'srt': enzh_srt,
                                                         'path_out': enzh_out}})  # 创建一个线程对象t1 子线程
                thread1.append(t2)
            for x in thread1:
                x.start()
            # 将最后一个子线程阻塞主线程，只有当所有子线程完成后主线程才能往下执行
            for x in thread1:
                x.join()
            try:
                f = open(path_out)
                f.close()
                if args.subtitle == 2:
                    f = open(enzh_out)
                    f.close()
            except IOError:
                print('file is not exist, maybe network disconnected')
    command = 'stty echo'
    subprocess.call(command, shell=True)