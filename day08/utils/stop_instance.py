#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from utils.tasks import ALICLOUD


def stop_host(instance_id):
    client = AcsClient(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])

    request = StopInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instance_id)
    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
