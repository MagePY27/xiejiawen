### 运维平台功能简介

**功能点：**
```
1.用户的增删改查
2.用户权限的增删改查
3.阿里云主机的信息获取与展示
4.登录系统与权限控制
```
一、用户管理系统

>1.用户基本信息展示，权限展示
>
>2.基于权限来限制用户的页面内容RBAC
>
>3.资产管理，标签编辑，主机信息
>
>4.基于阿里云API来操作主机

二、定时任务管理系统
```
**安装celery**
pip install django-celery
pip install redis==2.10.6
1.在app目录下创建tasks.py文件
2.在day08/day08目录下创建celery.py文件
3.在settings文件中注册app， djcelery
4.settings中其他配置
```python
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://192.168.99.105:6379/0' #redis中间件
BROKER_TRANSPORT = 'redis'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery.log" #需手动创建
~]$ python manage.py migrate

**安装redis 192.168.99.105**
~]# wget http://download.redis.io/releases/redis-5.0.8.tar.gz
~]# tar -zxf redis-5.0.8.tar.gz
~]# cd redis-5.0.8
~]# make

```
**celery.py文件**
```python
import os
import django
from celery import Celery
from django.conf import settings

# set the default Django settings module for the celery program

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day08.settings')

django.setup()

app = Celery('day08')

app.config_from_object('django.config:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

```
**tasks.py**
```python
from day08.celery import app
import traceback
import time
from django.contrib.auth.models import User

@app.task(name="create_user")
def useradd(username):
    try:
        user = User()
        user.username = username
        user.save()
        print('ok')
    except:
        print('ok')
        traceback.print_exc()

@app.task(name='测试任务')
def file():
    """
    测试任务，向文件写入字符
    """
    print('111')
    t = time.strtime("%Y-%m-%d %H:%M:%S", time.localtime())
    s = "Life is short , you need Python %s \r\n" %t
    f = open("logs/celery/task.txt", 'a+')
    f.write(s)
    f.close()
    return "Test is OK"
```

**启动celery**

celery -A day08 worker -l info
python manage.py celery beat

**supervisor管理celery任务**
```


![这是用户列表](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_list.jpg)
![这是增加用户](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_add.jpg)
![这是修改用户](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_modefy.jpg)
![这是删除用户](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_delete.jpg)
![这是用户登录](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_login.jpg)
![修改用户密码](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/change_password.jpg)
![重置密码](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/reset_user_password.jpg)
![这是仪表盘](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/index_page.jpg)
![这是权限列表](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/permission_list.jpg)
![权限修改](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/user_permission_modefy.jpg)
![这是组列表](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/group_list.jpg)
![组添加用户](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/group_add_user.jpg)
![添加组](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/group_add.jpg)
![标签类型](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/tag_type_list.jpg)
![标签列表](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/tag_list.jpg)
![添加标签类型](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/add_tag_type.jpg)
![添加标签](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/add_a_tag.jpg)
![主机信息表](https://github.com/MagePY27/xiejiawen/blob/master/day08/static/pro_picture/host_info_and_manage.jpg)
