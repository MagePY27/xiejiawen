from django.db import models
from django.contrib.auth import get_user_model
from cmdb.models import Host

User = get_user_model()


# Create your models here.
class Task(models.Model):
    """
    任务表
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='任务名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '任务系统'
        verbose_name_plural = '任务系统'
        default_permissions = ()
        permissions = (
            ('view_task', '查看任务'),
            ('add_task', '添加任务'),
            ('change_task', '编辑任务'),
            ('delete_task', '删除任务'),
            ('review_task', '审核任务'),
            ('release_task', '发布任务'),
            ('view_history', '查看历史')
        )

    def __str__(self):
        return self.name


class HistoricTask(models.Model):
    """
    历史任务（包含状态）
    """
    STATUS = (
        (-1, '已取消'),
        (0, '待审核'),
        (1, '未通过'),
        (2, '待发布'),
        (3, '已发布'),
    )

    task = models.ForeignKey('Task', verbose_name='任务', on_delete=models.CASCADE)
    dest_hosts = models.ManyToManyField('cmdb.Host', verbose_name='上线的主机', related_name='host_historic_tasks')
    content = models.TextField(verbose_name='更新内容')
    status = models.IntegerField(default=0, choices=STATUS)
    apply_user = models.ForeignKey(User, verbose_name='申请人', related_name='applied_tasks', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, null=True, verbose_name='审核人', related_name='reviewed_tasks', on_delete=models.CASCADE)
    review_at = models.DateTimeField(null=True, verbose_name='审核时间')
    review_notes = models.CharField(max_length=255, null=True, verbose_name='审核意见')
    publisher = models.ForeignKey(User, null=True, related_name='published_tasks', on_delete=models.CASCADE)
    publish_at = models.DateTimeField(null=True, verbose_name='发布时间')
    result = models.TextField(null=True, verbose_name='执行结果')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '历史任务'
        verbose_name_plural = verbose_name
        default_permissions = ()

    def __str__(self):
        return self.task.name