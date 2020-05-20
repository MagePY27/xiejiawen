from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

accessKeyId = "LTAI4G1aNcr6pRTwRLEn6T9H"
accessSecret = "ZGxVgA4KjSft6aVvbqzKl1DSBazzgm"

client = AcsClient(accessKeyId, accessSecret, 'cn-beijing')

request = DescribeInstancesRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)
print(str(response, encoding='utf-8'))

