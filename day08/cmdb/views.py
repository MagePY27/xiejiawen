from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.views.generic.base import View
from pure_pagination import PaginationMixin
from django.contrib import messages
# Create your views here.
from cmdb.models import Host,DataBase, Tag, Type
from django.conf import settings

import re
from utils.Aliyun_key import ALICLOUD
from utils.alisdk import ECSHandler, AliYunRDS
from .tasks import update_hosts_from_cloud, file, useradd

User = get_user_model()

class IndexView(View):

    def get(self, request):
        # 存钱
        file.delay()
        return HttpResponse("ok")


class TypeListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    标签类型列表
    """
    model = Type
    paginate_by = 5
    permission_required = 'cmdb.view_type'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_cn__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TypeAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建标签类型
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.add_type'
    success_message = '添加 %(name)s 类型成功'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        return reverse('cmdb:types')


class TypeEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    编辑标签
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.change_type'
    success_message = '标签类型 %(name_cn)s 编辑成功！'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        elif '_savedit' in self.request.POST:
            return reverse('cmdb:type-edit', kwargs={'pk': self.object.pk})
        else:
            return reverse('cmdb:types')


class TypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除类型
    """
    model = Type
    permission_required = 'cmdb.delete_type'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 标签类型删除成功！'.format(self.object.name_cn))
        return response

    def get_success_url(self):
        return reverse_lazy('cmdb:types')


class HostListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    主机列表
    """
    model = Host
    paginate_by = 10
    permission_required = 'cmdb.view_host'
    keyword = None
    slug = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_slug(self):
        self.slug = self.request.GET.get('tag')
        return self.slug

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.get_slug()
        if slug:
            queryset = queryset.filter(tags__name=slug)
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(instance_id__icontains=keyword) | Q(instance_name__icontains=keyword) |
                                       Q(description__icontains=keyword) | Q(hostname__icontains=keyword) |
                                       Q(public_ip__icontains=keyword) | Q(private_ip__icontains=keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['slug'] = self.slug
        context['types'] = Type.objects.all()
        context['tags'] = Tag.objects.all()
        context['hosts_count'] = Host.objects.count()
        return context

# class HostListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
#     model = Host
#     permission_required = 'cmdb.view_host'
#     paginate_by = 4
#     key_word = None
#
#     def get_keyword(self):
#         self.keyword = self.request.GET.get('keyword')
#         return self.keyword
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         keyword = self.get_keyword()
#         if keyword:
#             queryset = queryset.filter(Q(hostname__icontains=keyword) | Q(os_name__icontains=keyword))
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['keyword'] = self.keyword
#         return context


class AliyunSDK(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Host
    permission_required = 'cmdb.change_host'

    def get(self, request):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        # return data, True, len(instances) >= page_size
        instances = ecs.get_instances()[0]
        print(ecs.get_instances())
        for instance in instances:
            is_oldhost = Host.objects.filter(public_ip=instance['public_ip'], private_ip=instance['private_ip'])
            if not is_oldhost:
                Host.objects.create(**instance)
                res = {"code": 0, "msg": "主机列表刷新成功，有新增主机{}".format(instance['hostname'])}
            else:
                Host.objects.update(**instance)
                # object_list = Host.objects.all()
                res = {"code": 0, "msg": "刷新完成，主机数不变~"}
            return render(request, settings.JUMP_PAGE, res)


class HostTagAddView(LoginRequiredMixin, UpdateView):
    """
    给主机添加标签
    """
    template_name = 'cmdb/host_tags.html'
    model = Host
    fields = ('tags',)

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:host-tags-add', kwargs={'pk': self.object.pk})
        return reverse('cmdb:hosts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['hosts_tags'] = self.object.tags.all()
        return context


class HostAddByTagView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    通过标签添加主机或更新
    """
    permission_required = 'cmdb.change_tag'

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        hosts = Host.objects.all()
        selected_hosts = tag.host_set.all()
        context = {'hosts': hosts, 'selected_hosts': selected_hosts, 'tag': tag}
        return render(request, 'cmdb/host_add_by_tag.html', context=context)

    def post(self, request, pk):
        host_ids = request.POST.getlist('hosts')
        tag = get_object_or_404(Tag, pk=pk)
        if host_ids:
            hosts = Host.objects.filter(id__in=host_ids)
            tag.host_set.set(hosts)
        else:
            tag.host_set.clear()
        if '_savedit' in request.POST:
            return HttpResponseRedirect(reverse('cmdb:add-hosts', kwargs={'pk': pk}))
        return HttpResponseRedirect(reverse('cmdb:tags'))


class AssetsOverView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    资产大盘
    """
    model = Tag
    permission_required = 'cmdb.change_host'

    def get(self, request):
        aliyun_ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instances = aliyun_ecs.get_instances()[0]
        # 1.将阿里云主机统计数据加入多云资产的列表[{"name": "阿里云", "value", value}, {"name": "其他云", "value", value}]
        clouds_asset_count = []
        clouds_asset_aliyun = {
            "name": '阿里云',
            "value": len(instances)
        }
        clouds_asset_count.append(clouds_asset_aliyun)

        # 2.获取每个标签下的主机统计数据，并加入标签-主机统计数据列表[{"name": "标签名", "value": 对应标签的主机数}]
        business_line_host_nums = []
        tag_cloud = []
        tags = list(Tag.objects.all())
        print("tags:", tags, "number:", len(instances))
        for tag in tags:
            # tag_id = tag.id
            num = len(tag.host_set.all())
            print(type(tag), num)
            business_line_host = {
                "name": tag.name_cn,
                "value": num
            }
            business_line_host_nums.append(business_line_host)
            # 4.标签云，基于标签下主机数来自动生成权重
            tag_dict = {
                "text": tag.name_cn,
                "weight": num,
                "link": '/cmdb/hosts/?tag={}'.format(tag.name)
            }
            tag_cloud.append(tag_dict)
            print("标签:", tag_cloud)

        # 3.将主机按服务分类，数据库和服务器
        each_type_assets_count = []
        re_ecs = re.compile(r'^ecs.*$')
        re_rds = re.compile(r'^rds.*$')
        num_ecs = 0
        num_rds = 0
        num_other = 0
        for instance in instances:
            if re_ecs.match(instance['instance_type']):
                num_ecs += 1
            elif re_rds.match(instances['instance_type']):
                num_rds += 1
            else:
                num_other += 1
        each_type_assets_count = [{"name": '服务器', "value": num_ecs}, {"name": '数据库', "value": num_rds},
                                  {"name": '其他', "value": num_other}]

        # 最后，将所有数据统计到大字典overview中
        overview = {
            "clouds_asset_count": clouds_asset_count,
            "business_line_host_nums": business_line_host_nums,
            "each_type_assets_count": each_type_assets_count,
            "tag_cloud": tag_cloud,
        }
        return render(request, 'cmdb/assets_overview.html', {"overview": overview})






@require_GET
@login_required
def update_host_info(request):
    """
    更新主机信息
    :param request:
    :return:
    """
    update_hosts_from_cloud.delay()
    return HttpResponse('任务已提交到后台，请稍等片刻！')


@require_GET
@login_required
def assets_overview(request):
    """
    统计资产
    :param request:
    :return:
    """
    get_assets_from_cloud.delay()
    return HttpResponse("请稍后~")
    pass



class StopHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            ecs.stop_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在关机~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 1, "errmsg": "服务器繁忙，请稍后重试"}
        return render(request, settings.JUMP_PAGE, res)


class StartHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            res = {"code": 1, "errmsg": "主机正在运行，无需启动~"}
        elif instance.status == "Stopped":
            ecs.start_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在启动~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 2, "errmsg": "服务器繁忙，请稍后重试！"}
        return render(request, settings.JUMP_PAGE, res)


class RebootHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            ecs.reboot_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在重新启动~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        elif instance.status == "Stopped":
            ecs.start_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 1, "msg": "服务器繁忙，请稍后再试~"}
        return render(request, settings.JUMP_PAGE, res)