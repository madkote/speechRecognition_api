# virtualenv
## linux 安装python3.6
- 下载

``
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
``
- 解压

``
tar -zxf Python-3.6.4.tgz
``

- 配置 --prefix 指定安装路径 --enable-optimizations 稳定性优化参数

``
./configure --enable-optimizations --prefix=/usr/bin/python3.6.4
``
- 编辑和安装

``
make && make install
``
## 安装独立环境
``
pip install virtualenv
``
- 指定virtualenv的python版本,并创建独立环境,venv是环境名

``
virtualenv -p /path/to/python3.6 --no-site-packages venv
``
- 进入环境

``
source venv/bin/activate
``
- 退出环境

``
deactivate
``

