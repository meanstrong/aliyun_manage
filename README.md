# aliyun_manage
基于阿里云python-SDK对阿里云产品的操作

安装
------------
```
apt-get install rsync sshpass (这里以ubuntu为例)
git clone git@github.com:meanstrong/aliyun_manage.git
cd aliyun_manage
pip install -r pip_requirements.txt #建议使用virtualenv来部署
vi web/config.py #设置你的阿里云AccessKey和AccessSecret,以及http server端口等配置

python manage.py #start flask web app
```
