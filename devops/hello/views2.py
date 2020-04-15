from django.http import HttpResponse, Http404
from django.views.generic import View, TemplateView
from django.forms import Form
from hello.models import User
from django.shortcuts import render,reverse


def index(request):
    # users = User.objects.all()
    return render(request, 'hello/userlist.html', {"users": User.objects.all()})


class UserListView(View):
    model = User
    users = User.objects.all()

    def get(self, request):
        return render(request, 'hello/userlist.html', {"users": User.objects.all()})

    def post(self, request):
        return render(request, 'hello/userlist.html', {"users": User.objects.all()})

class UserAddView(View):
    pass

class UserDelView(View):
    pass

class UserModView(View):
    pass

