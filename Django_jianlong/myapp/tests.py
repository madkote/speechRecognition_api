from django.test import TestCase

# Create your tests here.
# print(1)
# audio_file="周杰伦 - Mojito的副本.mp3'"
# # audio_file='"周杰伦 - Mojito的副本.mp3'"
# audio_file = str(audio_file)
# print(audio_file)
# # print(type(audio_file))
# # res_1 =audio_file.startswith('"')
# # print(res_1)
# # res_2 =audio_file.endswith('"')
# # print(res_2)
# if (audio_file.startswith('"') or audio_file.startswith("'") or audio_file.endswith('"') or audio_file.endswith("'")):
#     res_1 = audio_file.replace('"','')
#     res = res_1.replace("'",'')
#     print(res)
#     print(type(res))

# from hashlib import md5

# test = "'周杰伦 - Mojito的副本.26998.wav'"
# print(eval(test))
# audio_file type: <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
data={'err_msg': 'request pv too much', 'err_no': 3305, 'sn': '258141401141593329826'}
print(data['err_msg'])
dev_pid_name=1536
if data['err_msg']=='request pv too much':
    dev_pid_name+=1

print(dev_pid_name)



