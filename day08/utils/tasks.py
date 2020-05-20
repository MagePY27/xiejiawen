import sys
import os

from utils.alisdk import ECSHandler

ALICLOUD = {
   'access_key_id': 'LTAI4G3WGzPc6SD95WdPabmV',
   'access_key': '5WOhOZ67xFzVKybTdvPysWEpGof62F',
   'region': 'cn-hangzhou',
}

def get_hosts_from_aliyun():
    """
    从阿里云获取ECS实例并入库
    :return:
    """
    ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
    instances, exception, next_page = ecs.get_instances(page_size=10)
    instances = dict(instances[0])
    print(instances)
    return instances


if __name__ == '__main__':
    get_hosts_from_aliyun()