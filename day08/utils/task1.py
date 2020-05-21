#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkvpc.request.v20160428.ActivateRouterInterfaceRequest import ActivateRouterInterfaceRequest

client = AcsClient('LTAI4G25yYUUkAUNnMK7dkTe', '5qlaC0BhzycSkSGHDjJm2V39q0UC74', 'cn-hangzhou')

request = ActivateRouterInterfaceRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))