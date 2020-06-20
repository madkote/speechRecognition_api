import subprocess
import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data-input', default='data_input', type=str, help='data input')
args = parser.parse_args()


if __name__=='__main__':
    data_input = args.data_input
    if os.path.isdir(data_input):
        list_input = os.listdir(data_input)
    else:
        data_input, filename = os.path.split(data_input)
        list_input = [filename]
    for i in range(0,len(list_input)):
        if list_input[i][-3:] == r'mp4'or list_input[i][-3:] == r'mkv':
            path_input = os.path.join(data_input, list_input[i])
            file_name = os.path.splitext(list_input[i])[0:-1]
            data_out = sys.path[0] + '/data_out/' + "".join(tuple(file_name)) + '/'
            os.makedirs(data_out, exist_ok=True)
            path_wav = data_out + '%s.wav'%(file_name)
            command = 'ffmpeg -y -i %s -ac 1 -ar 16000 %s' % (path_input, path_wav)
            subprocess.call(command, shell=True)
