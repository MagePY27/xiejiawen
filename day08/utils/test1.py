import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "day08.settings")

import django
django.setup()

from cmdb.models import Host
from utils.alisdk import ECSHandler

ALICLOUD = {
   'access_key': ('LTAI4G1aNcr6pRTwRLEn6T9H','ZGxVgA4KjSft6aVvbqzKl1DSBazzgm'),
   'region': 'cn-beijing'
}

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
        print(exception)
        print(next_page)
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

get_hosts_from_aliyun()
