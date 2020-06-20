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

# parser = argparse.ArgumentParser()
# parser.add_argument('--language', default='zh', type=str, help='recognition type zh,zhen or en,enzh')
# parser.add_argument('--subtitle', default=1, type=int, help='subtitle num 1 or 2')
# parser.add_argument('--interval', default=250, type=int,help='interval time ms')
# parser.add_argument('--data-input', default='data_input', type=str, help='data input')
# parser.add_argument('--data-out', default='data_out/', type=str, help='data out')
# args = parser.parse_args()




# 百度api翻译
class MachineTranlation:
    def __init__(self):
        # use for multi-thread
        self.q = queue.Queue()

    def translate_by_api_bing(self, from_lang: str='en', to_lang: str='zh', input: list=[]):
        ret = []
        res: List[str] = []
        lines: List[str] = input

        thread_count: int = 0
        thread_pool: List[Thread] = []

        start = time.time()
        for line in lines:
            t = Thread(target=self._do_translate_bing,
                       kwargs={'params': {'from': from_lang, 'to': to_lang, 'text': line}},
                       name=str(thread_count))
            thread_count += 1
            t.setDaemon(True)
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
            t.join()
        print('time consume by bing api: {}'.format(time.time() - start))

        while self.q.qsize() > 0:
            res.append(self.q.get())

        res.sort(key=lambda k: k[0])
        for _, text in res:
            ret.append(text)
        return ret

    def _do_translate_bing(self, params=None):
        url = 'cn.bing.com'
        conn = http.client.HTTPConnection(url)
        ct = current_thread()
        if len(params['text']) == 1:
            self.q.put((int(ct.getName()), ''))
            return

        # 向服务器发送请求
        method = "POST"
        req_url = "/ttranslate/"
        header_data = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        test_data = urllib.parse.urlencode({
            "from": params['from'],
            "to": params['to'],
            "text": params['text'],
        })
        conn.request(method=method, url=req_url, body=test_data, headers=header_data)

        # 获取响应消息体
        response = conn.getresponse()
        data: bytes = response.read()
        data: str = str(data, encoding='utf-8')
        data: Dict = eval(data)
        conn.close()

        if data['statusCode'] == 200:
            self.q.put((int(ct.getName()), data['translationResponse']))
        else:
            self.q.put((int(ct.getName()), 'translation fail'))
    def translate(self, temp_srt, temp_translate_srt):
        if args.language == 'en':
            from_lang = 'en'
            to_lang = 'zh'
        else:
            from_lang = 'zh'
            to_lang = 'en'
        with open(temp_srt, encoding='utf-8') as f:
            temp_srt_content = f.readlines()
        translate_srt=[]
        for i in range(len(temp_srt_content)):
            temp1 = temp_srt_content[i]
            if i % 4 == 2:
                translate_srt.append(temp1)
        #translate
        fanyiresult = self.translate_by_api_bing(from_lang, to_lang, translate_srt)
        result = []
        for i in range(len(fanyiresult)):
            fanyiresult[i] = fanyiresult[i].replace(",", " ")
            fanyiresult[i] = fanyiresult[i].replace("。", " ")
        for i in range(len(temp_srt_content)):
            temp1 = temp_srt_content[i]
            if i % 4 == 3:
                result.append(fanyiresult[i // 4]+'\n')
            result.append(temp1)
        with open(temp_translate_srt, 'w', encoding='utf-8') as f:
            for i in range(len(result)):
                f.write(result[i])

    # 计算消耗时间
    def cal_difftime(time1, time2):
        # 字符串转换为datetime类型
        times1 = datetime.strptime(str(time1), "%Y-%m-%d %H:%M:%S.%f")
        times2 = datetime.strptime(str(time2), "%Y-%m-%d %H:%M:%S.%f")
        # 利用datetime计算时间差并格式化输出
        timestamp = (times2 - times1).seconds
        m, s = divmod(timestamp, 60)
        h, m = divmod(m, 60)
        difftime = "%02d:%02d:%02d" % (h, m, s)
        return difftime
# 视频添加字幕
def video_srt(params=None):
    # 视频添加字幕
    path_input = params['path_input']
    path_srt = params['srt']
    file_srt = "subtitles=%s:force_style='Fontsize=14'" % (path_srt)
    path_out = params['path_out']
    command = 'ffmpeg -y -i %s -vf %s -shortest -strict -2 %s' % (path_input, file_srt, path_out)  # -shortest
    subprocess.call(command, shell=True)
# 主程序

# videoaddsubtitle 程序
def subtitle(language, filename):
    status = "ok"
    message = "0"
    #data_input = filename
    # if os.path.isdir(data_input):
    #     list_input = os.listdir(data_input)
    # else:
    #     data_input, filename = os.path.split(data_input)
    #     list_input = [filename]
    data_out = 'videoaddsubtitleapp/data_out/' + filename[:-4] + '/'
    os.makedirs(data_out, exist_ok=True) #ensure save folder exists
    file_url = ''
    if filename[-3:] == r'mp4' or filename[-3:] == r'mkv' or filename[-3:] == r'MOV':
        path_input = filename
        file_name = filename[:-4]
        print(file_name)
        # 原始视频提取音频
        path_wav = sys.path[0] + '/videoaddsubtitleapp/data_mkv/%s.wav' % (file_name)
        print(path_input,path_wav )
        command = 'ffmpeg -y -i %s -ac 1 -ar 16000 %s' % (path_input, path_wav)
        subprocess.call(command, shell=True)
        # 音频语音识别（阿里）
        command = '/home/jianlong/home/ali_c++/NlsSdkCpp2.0/demo/stDemo_srt_250 %s %s' \
                  % (language, path_wav)
        subprocess.call(command, shell=True)
        # 文本翻译
        temp_srt = sys.path[0] + '/videoaddsubtitleapp/data_mkv/%s.srt' % (file_name)  # source srt
        try:
            f = open(temp_srt)
            f.close()
        except IOError:
            print('temp.srt is not exist, maybe network disconnected')
            message = "2"
            status = "error"
        # if args.subtitle == 2:
        #     mt = MachineTranlation()
        #     enzh_srt = sys.path[0] + '/data_mkv/enzh%s.srt' % (file_name)  # translate
        #     mt.translate(temp_srt, enzh_srt)
        # 添加字幕，多线程
        path_out = os.path.join(data_out, "".join(tuple(filename)))
        #path_enzh_out = os.path.join(data_out, 'enzh' + "".join(tuple(list_input[i])))
        t1 = threading.Thread(target=video_srt,
                              kwargs={'params': {'path_input': path_input, 'srt': temp_srt,
                                                 'path_out': path_out}})  # 创建一个线程对象t1 子线程
        thread1 = []
        thread1.append(t1)
        # if args.subtitle == 2:
        #     t2 = threading.Thread(target=video_srt,
        #                           kwargs={'params': {'path_input': path_input, 'srt': enzh_srt,
        #                                              'path_out': path_enzh_out}})  # 创建一个线程对象t2 子线程
        #     thread1.append(t2)
        for x in thread1:
            x.start()
        # 将最后一个子线程阻塞主线程，只有当所有子线程完成后主线程才能往下执行
        for x in thread1:
            x.join()
        try:
            f = open(path_out)
            f.close()
        except IOError:
            print('temp.srt is not exist, maybe network disconnected')
            message = "1"
            status = "error"
        # file_url = "http://" + args.local_ip + ":" + str(args.port) + save_path_1 + nowTime + secondStamp + '.mp3'
        #file_url = "https://ai.urundata.com.cn:38001/api/videoaddsubtitle" + path_out
        file_url = "https://192.168.9.201" + ":27706/" + ''.join(path_out)
    response_data = json.dumps({"status": status, "message": message, "result": file_url})
    return response_data


if __name__=='__main__':

    # start = subtitle()
    # end = start.subtitle_api(args.language, args.data_input)
    # print(end)
    # 输入回显
    command = 'stty echo'
    subprocess.call(command, shell=True)