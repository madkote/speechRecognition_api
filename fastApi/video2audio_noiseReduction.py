import subprocess
import sys
import os
import argparse
import time
import re

class video2audioProcessing(object):
    # def __init__(self,video_input,wav_out):
    def __init__(self,video_input):
        self.video_input = video_input
        # self.wav_out = wav_out
    def video2audio(self):
        '''
        视频到音频
        '''
        data_input = self.video_input # 输入
        if os.path.isdir(data_input):
            list_input = os.listdir(data_input)
        else:
            data_input, self.filename = os.path.split(data_input)
            # print("data_input:",data_input)
            # print("filename:",self.filename)
            list_input = [self.filename]
        for i in range(0,len(list_input)):
            if list_input[i][-3:] == r'mp4'or list_input[i][-3:] == r'mkv':
                path_input = os.path.join(data_input, list_input[i])
                file_name = os.path.splitext(list_input[i])[0:-1]
                data_out = sys.path[0] + '/data_out/' + "".join(tuple(file_name)) + '/'
                os.makedirs(data_out, exist_ok=True)
                path_wav = data_out + '%s.wav'%(file_name) # 输出路径
                print("path_wav:",path_wav)
                command = 'ffmpeg -y -i %s -ac 1 -ar 16000 %s' % (path_input, path_wav)
                subprocess.call(command, shell=True)
        # return self.wav_out
        return path_wav

    def signalProcessing(self,inpath):
        '''
        处理音频，降噪和去除静音
        '''
        # from aukit import remove_noise, remove_silence
        # aunoise inpath outpath [in_format]
        t = int(time.time())
        # print("filename:",self.filename)
        # # out_filename = 
        # inpath = inpath
        # outpath = outpath
        # /Users/ccs/Desktop/myRepo/speechRecognition_api/fastApi/data_out/bali_1/bali_1.wav
        outpath = re.sub("bali_[1-9].wav","bali_{}.wav".format(t),inpath)
        in_format = "wav"
        command = 'aunoise %s %s [%s]' % (inpath, outpath,in_format)
        subprocess.call(command, shell=True)
        print("done")
        return outpath
    # def video2audio_removeNoise(self,video_path,wav_path):
    #     '''
    #     从视频到音频,并且音频去噪
    #     '''
    #     self.video2audio

        # return outpath
    def handlingText(self):
        """
        处理文本，文本正则化和汉字转拼音
        """
        pass

def video2audio_removeNoise(video_path):
    '''
    从视频到音频,并且音频去噪
    '''
    video_input= video_path
    processing = video2audioProcessing(video_input) # 实例化对象
    path_wav = processing.video2audio()
    # print(path_wav)
    outpath=processing.signalProcessing(path_wav)
    # print(outpath)
    return outpath

if __name__=="__main__":
    # video_input="./bali_1.mp4"
    # # outpath = "./data_out/bali_1/bali_2.wav"
    # processing = video2audioProcessing(video_input) # 实例化对象
    # path_wav = processing.video2audio()
    # print("path_wav:",path_wav)
    # outpath=processing.signalProcessing(path_wav)
    # print("outpath:",outpath)

    video_path="./bali_1.mp4"
    # wav_path="./bali_1_1.wav"
    res = video2audio_removeNoise(video_path)
    print(res)


