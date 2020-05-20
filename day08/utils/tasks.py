import sys
import os

from alisdk import ECSHandler

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
    instances, exception, next_page = ecs.get_instances(page_size=10)
    print(instances)
    return "hello"
