import re
from utils.alisdk import ECSHandler, AliYunRDS
from utils.Aliyun_key import ALICLOUD
from cmdb.models import Host, Tag


class DataGet(object):
    def __init__(self):
        self.aliyun_ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        self.instances = self.aliyun_ecs.get_instances()[0]
        self.clouds_asset_count = []
        self.business_line_host_nums = []
        self.each_type_assets_count = []
        self.tag_cloud = []
        self.aliyun_rds = None
        self.tencent_ecs = None
        self.huawei_ecs = None

    def get_aliyun_clouds_asset_count(self):
        """
        获取阿里云主机统计数据
        :return:
        """
        clouds_asset_aliyun = {
            "name": '阿里云',
            "value": len(self.instances)
        }
        self.clouds_asset_count.append(clouds_asset_aliyun)
        return self.clouds_asset_count

    def get_business_line_host_nums(self):
        """
        获取业务线主机和标签云
        :return:
        """
        tags = list(Tag.objects.all())
        for tag in tags:
            # 获取当前标签下主机的数量
            num = len(tag.host_set.all())
            business_line_host = {
                "name": tag.name_cn,
                "value": num
            }
            self.business_line_host_nums.append(business_line_host)
            # 标签云，基于标签下主机数来自动生成权重
            tag_dict = {
                "text": tag.name_cn,
                "weight": num,
                "link": '/cmdb/hosts/?tag={}'.format(tag.name)
            }
            self.tag_cloud.append(tag_dict)
        data_dict = {
                "business_line_host_nums": self.business_line_host_nums,
                "tag_cloud": self.tag_cloud
        }
        return data_dict

    def get_each_type_assets_count(self):
        """
        将主机按服务分类，数据库和服务器
        :return:
        """
        re_ecs = re.compile(r'^ecs.*$')
        re_rds = re.compile(r'^rds.*$')
        num_ecs = 0
        num_rds = 0
        num_other = 0
        for instance in self.instances:
            if re_ecs.match(instance['instance_type']):
                num_ecs += 1
            elif re_rds.match(instance['instance_type']):
                num_rds += 1
            else:
                num_other += 1
        self.each_type_assets_count = [{"name": '服务器', "value": num_ecs}, {"name": '数据库', "value": num_rds},
                                  {"name": '其他', "value": num_other}]
        return self.each_type_assets_count
