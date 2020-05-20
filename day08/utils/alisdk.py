import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import ModifyInstanceAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
from aliyunsdkrds.request.v20140815.DescribeSlowLogRecordsRequest import DescribeSlowLogRecordsRequest
from aliyunsdkrds.request.v20140815.DescribeDBInstanceAttributeRequest import DescribeDBInstanceAttributeRequest


class ECSHandler(object):
    """
    https://api.aliyun.com/new?spm=a2c4g.11186623.2.28.1b8c5671zgyWAu#/?product=Ecs
    """

    def __init__(self, access_key_id, secret_access_key, region_id="cn-shanghai"):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_id = region_id
        self.clt = self.connect()

    def connect(self):
        clt = AcsClient(self.access_key_id, self.secret_access_key, self.region_id)
        return clt

    def get_instances(self, page=1, page_size=10):
        """
        获取实例列表
        :param page: 页码
        :param page_size: 每一页数量
        :return:
        """
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format("json")
        request.set_PageSize(page_size)
        request.set_PageNumber(page)
        try:
            response_string = self.clt.do_action_with_exception(request)
        except Exception as e:
            return e.args, False, True
        else:
            response_obj = json.loads(response_string)
            data = []
            instances = response_obj['Instances']['Instance']
            for instance_obj in instances:
                tmp = self._process_instance_result(instance_obj)
                data.append(tmp)
            return data, True, len(instances) >= page_size

    def _get_amis(self, ami_id=None):
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format("json")
        request.set_PageSize(100)
        if ami_id:
            request.set_ImageId(ami_id)
        request.set_ImageOwnerAlias('self')

        try:
            response_string = self.clt.do_action_with_exception(request)
            response = json.loads(response_string)
        except Exception as e:
            return {}
        else:
            return {str(x['ImageId']): str(x['ImageName']) for x in response['Images']['Image']}


    def _process_instance_result(self, instance):

        if instance['InstanceNetworkType'] == 'vpc':
            public_ip = ",".join(instance['PublicIpAddress']['IpAddress'])
            private_ip = ",".join(instance['VpcAttributes']['PrivateIpAddress']['IpAddress'])

        elif instance['InstanceNetworkType'] == 'classic':
            public_ip = ','.join(instance['PublicIpAddress']['IpAddress'])
            private_ip = ",".join(instance['InnerIpAddress']['IpAddress'])

        else:
            public_ip, private_ip = None, None

        instance_id = instance['InstanceId']
        image_id = instance['ImageId']
        _ami_map = self._get_amis(image_id)
        image_name = _ami_map.get(image_id, '')
        return {
            'image_id': image_id,
            'instance_id': instance_id,
            'instance_name': instance['InstanceName'],
            'instance_type': instance['InstanceType'],
            "instance_charge_type": instance['InstanceChargeType'],
            'description': instance['Description'],
            'hostname': instance['HostName'],
            'status': instance['Status'],
            'public_ip': public_ip,
            'private_ip': private_ip,
            'creation_time': instance['CreationTime'].replace('T', ' ').rstrip('Z'),
            'expired_time': instance['ExpiredTime'].replace('T', ' ').rstrip('Z'),
            'os_type': instance['OSType'],
            'os_name': instance['OSName'],
            "memory": instance['Memory'] / 1024,
            "cpu": instance['Cpu'],
            'region_id': instance['RegionId'],
            'zone_id': instance['ZoneId'],
        }



class AliYunRDS:
    def __init__(self, access_key, access_secret, region):
        self.access_key = access_key
        self.access_secret = access_secret
        self.region = region
        self._params = {}
        self.client = self.get_client()

    def get_client(self):
        client = AcsClient(self.access_key, self.access_secret, self.region)
        return client

    def add_query_param(self, k, v):
        self._params[k] = v

    def get_query_params(self):
        return self._params

    def set_start_time(self, start_time):
        self.add_query_param('StartTime', start_time)

    def get_start_time(self):
        return self.get_query_params().get('StartTime')

    def set_end_time(self, end_time):
        self.add_query_param('EndTime', end_time)

    def get_end_time(self):
        return self.get_query_params().get('EndTime')

    def set_instance_id(self, instance_id):
        self.add_query_param('InstanceId', instance_id)

    def get_instance_id(self):
        return self.get_query_params().get('InstanceId')

    def get_instances(self, page=1, page_size=30):
        """
        获取实例列表
        :return:
        """
        request = DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.set_PageNumber(page)
        request.set_PageSize(page_size)
        try:
            response = self.client.do_action_with_exception(request)
            response = json.loads(str(response, encoding='utf-8'))
            instances = response['Items']['DBInstance']
            data = []
            for instance in instances:
                handled_result = self._process_result(instance['DBInstanceId'])
                data.append(handled_result)
            return {'code': 'SUCCESS', 'msg': '成功', 'data': data, 'next_page': len(instances) == page_size}
        except ServerException as e:
            return {'code': e.get_error_code(), 'msg': e.get_error_msg()}
        except ClientException as e:
            return {'code': e.get_error_code(), 'msg': e.get_error_msg()}

    def _process_result(self, instance_id):
        """
        处理实例数据，组合成数据库需要的字段
        :param instance_id:
        :return:
        """
        instance = self.get_instance_attribute(instance_id)
        region_id = instance['RegionId']
        zone_id = instance['ZoneId']
        instance_id = instance['DBInstanceId']
        description = instance['DBInstanceDescription']
        engine = instance['Engine']
        connection_address = instance['ConnectionString']
        port = instance['Port']
        cpu = instance['DBInstanceCPU']
        memory = instance['DBInstanceMemory']
        storage = instance['DBInstanceStorage']
        max_iops = instance['MaxIOPS']

        return {'region_id': region_id, 'zone_id': zone_id, 'instance_id': instance_id, 'description': description,
                'engine': engine, 'connection_address': connection_address, 'port': port,
                'cpu': cpu, 'memory': memory, 'storage': storage, 'max_iops': max_iops}

    def get_instance_attribute(self, instance_id):
        """
        通过instance ID获取RDS实例的描述信息
        :param instance_id:
        :return:
        """
        request = DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(instance_id)

        response = self.client.do_action_with_exception(request)
        response = json.loads(str(response, encoding='utf-8'))

        return response['Items']['DBInstanceAttribute'][0]

    def get_slow_logs(self, page=1, page_size=30):
        """
        获取慢日志
        :param page: 页码
        :param page_size: 每页条数
        :return:
        """
        request = DescribeSlowLogRecordsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(self.get_instance_id())
        request.set_StartTime(self.get_start_time())
        request.set_EndTime(self.get_end_time())
        request.set_PageNumber(page)
        request.set_PageSize(page_size)

        try:
            response = self.client.do_action_with_exception(request)
            response = json.loads(str(response, encoding='utf-8'))
            sql_slow_records = response['Items']['SQLSlowRecord']
            instance_name = self.get_instance_attribute(self.get_instance_id())['DBInstanceDescription']
            data = []
            for record in sql_slow_records:
                record['InstanceName'] = instance_name
                data.append(record)
            return {'code': 'SUCCESS', 'msg': '成功', 'data': data, 'next_page': len(data) == page_size}
        except ServerException as e:
            return {'code': e.get_error_code(), 'msg': e.get_error_msg()}
        except ClientException as e:
            return {'code': e.get_error_code(), 'msg': e.get_error_msg()}



