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

# 视频到音频（降噪处理）接口
+ 运行后台
```
cd ./fastApi/
uvicorn main:app --port 7000 --reload
```
+ 接口
```
http://127.0.0.1:7000/video2audio/
方法：post
字段：video_path 类型：文件
``` 
![Umj8eS.png](https://s1.ax1x.com/2020/07/09/Umj8eS.png)

# 会有帮助的文档
+ [Python Web 框架之FastAPI](https://www.jianshu.com/p/d01d3f25a2af)
+ [使用FastAPI框架快速构建高性能的api服务](https://blog.csdn.net/u013421629/article/details/104500192)
+ [fastapi(十二)-表单数据和文件上传](https://blog.csdn.net/vanexph/article/details/104983660)
+ ![UVyfpV.png](https://s1.ax1x.com/2020/07/08/UVyfpV.png)
