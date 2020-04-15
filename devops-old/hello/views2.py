from django.http import HttpResponse
from django.shortcuts import  render
from django.views.generic import View, TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView
from hello.models import User
from datetime import datetime, timezone

def index(request): #条件过滤方式
    if request.method == 'GET':
        return HttpResponse('get')
    elif request.method == 'POST':
        return HttpResponse('post')
    elif request.method == 'PUT':
        return HttpResponse('put')
    elif request.method == 'DELETE':
        return HttpResponse('delete')


class IndexView(View): #类视图方式
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')

    def delete(self, request):
        return HttpResponse('delete')

    def put(self, request):
        return HttpResponse('put')

    def trace(self, request):
        pass

    def patch(self, request):
        pass

    def head(self, request):
        pass

    def options(self, request):
        pass


class IndexView1(View):
    template_name = 'hello/index.html'
    model = User
    keyword = ""

    def get(self, request):
        users = User.objects.all()
        return render(request, 'hello/index.html' ,{"users":users})

    def post(self, request):
        data = request.POST.dict()
        User.objects.create(**data)
        users = User.objects.all()
        return render(request, 'hello/index.html', {"users": users})

class IndexView2(TemplateView):
    template_name = "hello/useradd.html" #只返回空模板，但是没数据,因此模板视图适用于这个
    model = User

    def get_success_url(self):
        return reversed('hello:index1')

    def get_context_data(self, **kwargs):
        context = super(IndexView2, self).get_context_data(**kwargs)
        context['users'] = User.objects.all() #获取数据
        return context

    def post(self, request):
        data = request.POST.dict()
        User.objects.create(**data)
        users = User.objects.all()
        return render(request, 'hello/index.html', {"users":users})

class IndexView3(ListView):
    """
    ListView适用于以下场景:
    1.getlist列出所有数据
    2.create创建数据
    """
    #http://ip/hello/index3/?keyword=kk
    # template_name = 'hello/index.html' #制定模版文件，可不写
    model = User #object_lsit = User.objects.all()
    context_object_name = "users" #自定义传给前端的变量,index.html中使用的变量名为users因此此处为users
    keyword = ""                   #或者不用改名，前端使用object_list变量也可以接收数据

    def get_queryset(self): #搜索
        queryset = super(IndexView3, self).get_queryset()
        print(queryset)
        self.keyword = self.request.GET.get("keyword", "")
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        #继承基础的ListView类
        context = super(IndexView3, self).get_context_data(**kwargs)
        #在父类的基础上再额外添加数据到object_list中
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        data = request.POST.dict()
        User.object.create(**data)
        users = User.object.all()
        return render(request, 'hello/index.html', {"users":users})

class IndexView4(DetailView):
    """
    获取某条记录的ID，适用于下面三种场景，核心是拿到url中的id
    getone:获取当前记录数据
    update:更新...
    delete:删除...
    """
    template_name = 'hello/index.html'
    model = User
    context_object_name = "user" #定义存储返回结果的对象名，也可不写，默认使用object作为变量名传参

    def get_context_data(self, **kwargs):
        print(kwargs)
        #返回一条数据**kwargs为where条件，即url中传入的pk主键条件
        context = super(IndexView4, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        print(context)
        return context

class IndexView5(CreateView):
    """
    添加用户
    """
    template_name = 'hello/useradd.html'
    model = User
    fields = ('name', 'password', 'age', 'sex')

    def get_context_data(self, **kwargs):
        context = super(IndexView5, self).get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

class IndexView6(UpdateView):
    template_name = 'hello/usermod.html'
    model = User
    fields = ('name', 'password', 'age', 'sex')

    def get_success_url(self):
        return reversed('hello:userlist', kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(IndexView6, self).get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

    def post(self, request):
        data = request.POST.dict()
        User.objects.create(**data)
        users = User.objects.all()
        return render(request, 'hello/index.html', {"users":users})

class IndexView7(DeleteView, View):
    template_name = 'hello/userdel.html'
    model = User
    #
    def get_success_url(self):
        return reversed('hello:index1')

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView7, self).get_context_data(**kwargs)
    #     context["users"] = User.objects.all()
    #     return context

    def post(self, request):
        data = request.POST.dict()
        User.objects.create(**data)
        users = User.objects.all()
        return render(request, 'hello/index.html', {"users":users})