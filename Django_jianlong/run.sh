source /home/barfoo/web/speech_recognition_api/py36venv/bin/activate
nohup python manage.py runserver 0.0.0.0:27705 & 




# my
+ [tensorflow 对应 的keras 版本， 版本不匹配会出现很多问题](https://blog.csdn.net/yeyang911/article/details/84968473)

ps -ef | grep 27704 | grep -v root | awk '{print $2}' | xargs kill -9

中文本地接口：http://0.0.0.0:27704/zhRecognition/
现在 /Users/ccs/Desktop/speech_recognition_api

conda activate speechrecognition