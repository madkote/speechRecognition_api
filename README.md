# speechRecognition_api
语音识别接口

+ [中文语音识别接口](https://ai.urundata.com.cn:38001/api/speech_recognition/zhRecognition/)
+ ![N2Tbj0.png](https://s1.ax1x.com/2020/06/28/N2Tbj0.png)
+ [英文语音识别接口](https://ai.urundata.com.cn:38001/api/speech_recognition/enRecognition/)
+ ![N2793R.png](https://s1.ax1x.com/2020/06/28/N2793R.png)

# 前期准备

+ 安装环境
``` 
ps -ef | grep 端口号 | awk '{print $2}' | xargs kill -9
cd /Users/ccs/Desktop/myRepo/speechRecognition_api/Django_jianlong/
pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com

``` 
+ 运行
```
python manage.py runserver 0.0.0.0:27705 
or 
source ./run.sh
```

# 可能出现的问题
+ [tensorflow 对应 的keras 版本， 版本不匹配会出现很多问题](https://blog.csdn.net/yeyang911/article/details/84968473)
+ [python baidu-aip语音识别错误request pv too much](https://blog.csdn.net/w5688414/article/details/106398264/)

# 远程服务器运行
```
tmux a -t 162
```