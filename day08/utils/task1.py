#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkvpc.request.v20160428.ActivateRouterInterfaceRequest import ActivateRouterInterfaceRequest

client = AcsClient('LTAI4G3WGzPc6SD95WdPabmV', '5WOhOZ67xFzVKybTdvPysWEpGof62F', 'cn-hangzhou')

request = ActivateRouterInterfaceRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))