# ffmpeg安装步骤
## 在root目录下创建安装目录
```
mkdir developer
ls developer 
mkdir ffmpeg
```
## 选择要安装的ffmpeg版本
- 在自己的文件夹下下载如 install文件夹下下载
```
wget https://ffmpeg.org/releases/ffmpeg-4.1.tar.bz2
```
- 解压
```
tar -xjvf ffmpeg-4.1.tar.bz2
```
- 切换到解压好的目录中
```
cd ffmpeg-4.1/
```
- 先安装 yasm ,如果没有yum,先安装yum
```
yum install yasm
```
- 如果个人目录安装不了,如果权限不够请使用root
```
sudo apt-get install yasm
```
- 安装完毕后，注意这个prefix，是将ffmpeg安装到prefix指定的目录下面
```
./configure --enable-shared --prefix=/developer/ffmpeg
```
- 编译，如果编译不通过，请用root,编译时间较长，请耐心等待
```
make 
make install
```
- root 权限，新建ffmpeg.conf，在这个文件中写入/developer/ffmpeg/lib
```
vim /etc/ld.so.conf.d/ffmpeg.conf 
```
- 保存退出后使配置生效
```
ldconfig
```
- 查看版本和是否安装成功
```
cd developer/ffmpeg/bin
./ffmpeg -version
```
- 全局调用，配置环境变量
```
vim /etc/profile
编辑，添加：export PATH=/developer/ffmpeg/bin
```