from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Type(models.Model):
    """
    标签类型
    """
    name = models.CharField(max_length=100, verbose_name='类型名称')
    name_cn = models.CharField(max_length=100, verbose_name='中文名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签类型'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_type', '查看标签类型'),
            ('add_type', '添加标签类型'),
            ('change_type', '编辑标签类型'),
            ('delete_type', '删除标签类型'),
        )

    def __str__(self):
        return self.name_cn


class Tag(models.Model):
    """
    标签
    """
    type = models.ForeignKey('Type', verbose_name='类型', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='标签名称')
    name_cn = models.CharField(max_length=100, verbose_name='中文名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_tag', '查看标签'),
            ('add_tag', '添加标签'),
            ('change_tag', '编辑标签'),
            ('delete_tag', '删除标签'),
        )

    def __str__(self):
        return self.name_cn


CLOUD = (
    ('aliyun', '阿里云'),
    ('qcloud', '腾讯云'),
)

class Host(models.Model):
    """
    主机包括阿里云的ECS, 腾讯云的CVM等
    """

    STATUS = (
        ('Running', '运行中'),
        ('Starting', '启动中'),
        ('Stopping', '停止中'),
        ('Stopped', '已停止')
    )

    CHARGE_TYPE = (
        ('PrePaid', '预付费'),
        ('PostPaid', '后付费')
    )

    public_cloud = models.CharField(max_length=20, choices=CLOUD, default='aliyun', verbose_name='云主机类型')
    instance_id = models.CharField(max_length=22,  verbose_name='实例ID')
    instance_name = models.CharField(max_length=22, verbose_name='实例的显示名称')
    description = models.CharField(max_length=128, null=True, blank=True, verbose_name='实例的描述')
    image_id = models.CharField(max_length=50, verbose_name='镜像ID')
    region_id = models.CharField(max_length=30, verbose_name='实例所属地域ID')
    zone_id = models.CharField(max_length=30, verbose_name='实例所属可用区')
    cpu = models.IntegerField(verbose_name='CPU核数')
    memory = models.IntegerField(verbose_name='内存大小，单位: GB')
    instance_type = models.CharField(max_length=30, verbose_name='实例资源规格')
    status = models.CharField(max_length=8, choices=STATUS, default='Running', verbose_name='实例状态')
    hostname = models.CharField(max_length=23, blank=True, null=True, verbose_name='实例机器名称')
    public_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='公网IP')
    private_ip = models.GenericIPAddressField(verbose_name='私网IP')
    os_type = models.CharField(max_length=10, default='linux', verbose_name='操作系统类型')
    os_name = models.CharField(max_length=20, default='', verbose_name='操作系统名称')
    instance_charge_type = models.CharField(max_length=8, default='PrePaid', choices=CHARGE_TYPE,
                                            verbose_name='实例的付费方式')
    creation_time = models.DateTimeField(verbose_name='创建时间')
    expired_time = models.DateTimeField(verbose_name='过期时间')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_host', '查看主机'),
            ('change_host', '更新主机信息'),
        )

    def __str__(self):
        return self.instance_name


class DataBase(models.Model):
    """
    云数据库
    """
    public_cloud = models.CharField(max_length=20, choices=CLOUD, default='aliyun', verbose_name='云主机类型')
    region_id = models.CharField(max_length=30, verbose_name='实例所属地域ID')
    zone_id = models.CharField(max_length=30, verbose_name='实例所属可用区')
    instance_id = models.CharField(max_length=20, verbose_name='实例ID', db_index=True)
    description = models.CharField(max_length=100, verbose_name='实例描述信息')
    engine = models.CharField(max_length=20, verbose_name='数据库类型')
    cpu = models.IntegerField(verbose_name='CPU核数')
    memory = models.IntegerField(verbose_name='内存')
    max_iops = models.IntegerField(verbose_name='最大的IOPS')
    storage = models.IntegerField(verbose_name='存储空间(GB)')
    connection_address = models.CharField(max_length=100, verbose_name='数据库连接地址')
    port = models.IntegerField(verbose_name='端口号')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '数据库'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_database', '查看数据库'),
            ('change_database', '更新数据库')
        )

    def __str__(self):
        return self.description
