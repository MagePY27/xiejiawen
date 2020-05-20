import sys
import os

from utils.alisdk import ECSHandler

ALICLOUD = {
   'access_key_id': 'LTAI4GFELsoox7E1NsKLNnfz',
   'access_key': 'PS0Dwg5KjPnO4ivk9YeHinQ5lDLcCp',
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