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



# api翻译
class MachineTranlation:
    def __init__(self):
        # use for multi-thread
        self.q = queue.Queue()

    @staticmethod
    def translate_by_api(to_lang: str='zh', input: str='apple') -> str:
        ret = ''
        appid = '20190605000305156'         # appid
        secretKey = '35gcTMJqQF0stnj3TVTS'  # 密钥

        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

        http_client = None
        salt = random.randint(32768, 65536)
        sign = appid + input + str(salt) + secretKey
        m1 = hashlib.new('md5')
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        url = url + '?q=' + urllib.request.quote(
            input) + '&from=' + 'auto' + '&to=' + to_lang + '&appid=' + appid + '&salt=' + str(salt) + '&sign=' + sign

        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', url)
            # response是HTTPResponse对象
            response = http_client.getresponse()
            result = response.read()

            data = json.loads(result)
            output = data['trans_result'][0]['dst']
            ret = output

        finally:
            if http_client:
                http_client.close()

        return ret

    def translate_by_api_bing(self, from_lang: str='en', to_lang: str='zh', input: list=[]) -> str:
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
        req_url = "/ttranslatev3/"
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
        data: Dict = json.loads(data)
        # print(type(data))
        # print(data)
        conn.close()

        if isinstance(data, list) and 'translations' in data[0].keys():
        # if data['statusCode'] == 200:
            self.q.put((int(ct.getName()), data[0]['translations'][0]['text']))
        else:
            # 失败手动重试1次
            time.sleep(0.2)
            conn.request(method=method, url=req_url, body=test_data, headers=header_data)
            response = conn.getresponse()
            data: bytes = response.read()
            data: Dict = json.loads(data)
            if isinstance(data, list) and 'translations' in data[0].keys():
                self.q.put((int(ct.getName()), data[0]['translations'][0]['text']))
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
                result.append(fanyiresult[i // 4])
            result.append(temp1)
        with open(temp_translate_srt, 'w', encoding='GBK') as f:
            for i in range(len(result)):
                f.write(result[i])

# 主程序

# videoaddsubtitle 程序
def subtitle(language, filename):
    status = "ok"
    message = "0"
    data_out = sys.path[0]+'/videoaddsubtitleapp/data_out/' + filename[:-4] + '/'
    os.makedirs(data_out, exist_ok=True) #ensure save folder exists
    url = ''
    if filename[-3:] == r'mp4' or filename[-3:] == r'mkv' or filename[-3:] == r'MOV':
        path_input = filename
        file_name = filename[:-4]
        # 原始视频提取音频
        path_wav = data_out + '%s.wav' % (file_name)
        command = 'ffmpeg -y -i %s -ac 1 -ar 16000 %s' % (path_input, path_wav)
        subprocess.call(command, shell=True)
        print(path_wav)
        # 音频语音识别（阿里）
        command = '/home/barfoo/web/speech_recognition_api/install/NlsSdkCpp2.0/demo/stDemo_srt %s %s' \
                  % (language, path_wav)
        subprocess.call(command, shell=True)
        # 文本翻译
        path_srt = data_out + '%s.srt' % (file_name) # source srt
        print(path_srt)
        # try:
        #     f = open(path_srt)
        #     f.close()
        # except IOError:
        #     print('temp.srt is not exist, maybe network disconnected')
        #     message = "2"
        #     status = "error"
        # 添加字幕，多线程
        path_out = os.path.join(data_out, ''.join(tuple(filename)))
        file_srt = "subtitles=%s:force_style='Fontsize=10'" % (path_srt)
        command = 'ffmpeg -y -i %s -vf %s -strict -2 %s' % (path_input, file_srt, path_out)  # -shortest
        subprocess.call(command, shell=True)
        print(path_out)
        #path_enzh_out = os.path.join(data_out, 'enzh' + "".join(tuple(list_input[i])))
        # try:
        #     f = open(path_out)
        #     f.close()
        # except IOError:
        #     print('temp.srt is not exist, maybe network disconnected')
        #     message = "1"
        #     status = "error"
        video_url = 'https://ai.urundata.com.cn:38001/api/speech_recognition/static/data_out/' + file_name + '/%s.srt' % (file_name)
        subtitle_url = 'https://ai.urundata.com.cn:38001/api/speech_recognition/static/data_out/' + file_name +'/%s'% (filename)
        url = {'video_url': video_url, 'subtitle_url': subtitle_url}
    response_data = json.dumps({"status": status, "message": message, "url": url})
    return response_data

if __name__=='__main__':
    result = subtitle('zh', './bali.mp4')
    print(result)
    command = 'stty echo'
    subprocess.call(command, shell=True)