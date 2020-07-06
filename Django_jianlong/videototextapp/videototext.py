#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import subprocess
import json

def writeLmk(fileName, landmarks):
    fp = open(fileName, 'w+', encoding='utf-8')
    fp.write("[{" + '\r\n')
    for i in range(len(landmarks)):
        id = landmarks[i].strip().split('\t')
        if len(id)==4:
            onebest=id[3]
        else:
            onebest=""
        si, bg, ed = id[0],id[1],id[2]
        fp.write('\t'+"\"bg\": \"%s\""%bg + '\r\n')
        fp.write('\t' + "\"ed\": \"%s\"" % ed + '\r\n')
        fp.write('\t' + "\"nc\": \"1.0\"" + '\r\n')
        fp.write('\t' + "\"onebest\": \"%s\"" % onebest + '\r\n')
        fp.write('\t' + "\"si\": \"%s\"" % si + '\r\n')
        fp.write('\t' + "\"speaker\": \"0\""  + '\r\n')
        if i < len(landmarks)-1:
            fp.write("}, {" + '\r\n')
    fp.write("}]")
    fp.close()
def translate(path_text):
    with open(path_text, 'r',encoding='utf-8') as f:
        text_content = f.readlines()
    result = []
    for i in range(len(text_content)):
        text_dict = {"bg": "0",
                     "ed": "0",
                     "nc": "1.0",
                     "onebest": "0",
                     "si": "0",
                     "speaker": "0"
                     }
        id= text_content[i].strip().split('\t')
        if len(id)==4:
            onebest=id[3]
        else:
            onebest=""
        si, bg, ed = id[0],id[1],id[2]
        text_dict["bg"] = bg
        text_dict["ed"] = ed
        text_dict["onebest"] = onebest
        text_dict["si"] = si
        result.append(text_dict)
    return result
def video_to_text(language, filename):
    status = "ok"
    message = "0"
    print("language:",language)
    print("filename:",filename)
    #data_out = '/home/barfoo/web/speech_recognition_api/django/Django_jianlong/videoaddsubtitleapp/data_out/' + filename[:-4] + '/'
    data_out = os.path.join(sys.path[0], 'static/out/'+filename[:-4])
    print(data_out)
    os.makedirs(data_out, exist_ok=True) #ensure save folder exists
    print(data_out)
    if filename[-3:] == r'mp4' or filename[-3:] == r'mkv' or filename[-3:] == r'MOV':
        path_input = filename
        file_name = filename[:-4]
        print(file_name)
        # 原始视频提取音频
        path_wav = os.path.join(data_out, '%s.wav' % (file_name))
        print(path_wav)
        command = 'ffmpeg -y -i %s -ac 1 -ar 16000 %s' % (path_input, path_wav)
        subprocess.call(command, shell=True)
        # 音频语音识别（阿里）
        # command = '/home/barfoo/web/speech_recognition_api/install/NlsSdkCpp2.0/demo/stDemo_txt_250 %s %s' \
        #           % (language, path_wav)
        command = '/home/barfoo/web/speech_recognition_api/install/NlsSdkCpp3.X/demo/stDemo %s %s' \
                  % (language, path_wav)
        # command = '/home/jianlong/home/ali_c++/NlsSdkCpp2.0/demo/stDemo_txt %s %s' \
        #           % (language, path_wav)
        subprocess.call(command, shell=True)
        path_text = os.path.join(data_out, '%s.txt' % (file_name))
        try:
            f = open(path_text)
            f.close()
        except IOError:
            print('temp.txt is not exist, maybe network disconnected')
            message = "1"
            status = "error"
        #转换成需要格式
        result = translate(path_text)
        # with open(path_text, 'r',encoding='utf-8') as f:
        #     text_content = f.readlines()
        # path_transform_text = os.path.join(data_out, '%s99.txt' % (file_name))
        # writeLmk(path_transform_text, text_content)
        # try:
        #     f = open(path_text)
        #     f.close()
        # except IOError:
        #     print('transform.txt is not exist, maybe network disconnected')
        #     message = "2"
        #     status = "error"
        # text_url = 'https://ai.urundata.com.cn:38001/api/speech_recognition/static/out/' + file_name + '/%s99.txt' % (
        #    file_name)
        # text_url = 'http://192.168.9.201:27705/static/out/' + file_name + '/%s99.txt' % (
        #     file_name)
    #response_data = json.dumps({"status": status, "message": message, "result": result}, ensure_ascii=False)
    response_data = {"status": status, "message": message, "result": result}
    return response_data
