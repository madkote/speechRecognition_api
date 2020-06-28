import subprocess
from datetime import datetime
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--language', default='en', type=str, help='recognition type zh,zhen or en,enzh')
parser.add_argument('--interval', default=250, type=int, help='interval time ms')
parser.add_argument('--data-input', default='data_input', type=str, help='data input')
args = parser.parse_args()
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

if __name__=='__main__':
    start_time = datetime.now()
    data_input = args.data_input
    if os.path.isdir(data_input):
        list_input = os.listdir(data_input)
    else:
        data_input, filename = os.path.split(data_input)
        list_input = [filename]
    for i in range(0, len(list_input)):
        if list_input[i][-3:] == r'mp4'or list_input[i][-3:] == r'mkv'or list_input[i][-3:] == r'MOV':
            path_input = os.path.join(data_input, list_input[i])
            file_name = os.path.splitext(list_input[i])[0:-1]
            data_out = sys.path[0] + '/data_out/' + "".join(tuple(file_name)) + '/'
            os.makedirs(data_out, exist_ok=True)
            path_wav = data_out + '%s.wav'%(file_name)
            command = '/home/barfoo/web/speech_recognition_api/install/NlsSdkCpp2.0/demo/stDemo_srt %s %s'% (args.language, path_wav)
            subprocess.call(command, shell=True)
    end_time = datetime.now()
    print(cal_difftime(start_time, end_time))

    
