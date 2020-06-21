# speechRecognition_api
语音识别接口


pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com
pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple --trusted-host pypi.douban.com wrapt
python manage.py runserver 127.0.0.1:27705

+ [[python] 安装TensorFlow问题 解决Cannot uninstall 'wrapt'. It is a distutils installed project](https://www.cnblogs.com/conver/p/11141176.html)

pip install keras -U --pre -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com
pip install --upgrade tensorflow -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com

fg [10]+ 


python manage.py runserver 0.0.0.0:27705
ps -ef | grep node | awk '{print $2}' | xargs kill -9
