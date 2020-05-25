from day08.celery import app
from cmdb.models import Host
from utils.alisdk import ECSHandler
import time

ALICLOUD = {
   'access_key': ('LTAI4G1aNcr6pRTwRLEn6T9H','ZGxVgA4KjSft6aVvbqzKl1DSBazzgm'),
   'region': 'cn-beijing'
}

@app.task(name='测试任务')
def file(): 
    """
    测试任务：向文件写入字符串
    """
    print("111")
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    s = "Life is short,you need Python %s \r\n" % t
    f = open("/tmp/task.txt", 'a')
    f.write(s)
    f.close()
    return 'Test is OK'


@app.task(name='创建用户')
def useradd(username): 
    """
    创建用户
    """
    print(username)
    return username

def get_hosts_from_aliyun():
    """
    从阿里云获取ECS实例并入库
    :return:
    """
    ecs = ECSHandler(*ALICLOUD['access_key'], ALICLOUD['region'])
    page = 1
    while True:
        instances, exception, next_page = ecs.get_instances(page=page, page_size=10)
        print(instances)
        # print(exception)
        # print(next_page)
        if instances:
            for i in instances:
                i['public_cloud'] = 'aliyun'
                print(i)
                host, created = Host.objects.update_or_create(instance_id=i['instance_id'], defaults=i)
                if created:
                    print('阿里云 {} 新主机入库'.format(host.instance_name))
                else:
                    print('阿里云 {} 更新主机入库'.format(host.instance_name))
            page += 1
            if not next_page:
               break
    return True

# get_hosts_from_aliyun()

@app.task(name='更新服务器资产信息')
def update_hosts_from_cloud():
    """
    从阿里云和腾讯云上获取主机信息并入库
    :return:
    """
    aliyun_success = get_hosts_from_aliyun()
    if aliyun_success:
        return '更新资产信息成功'
    else:
        return '更新资产信息失败'


