from django.views import View
from django.forms import Form
from django.views.generic import TemplateView
from django.shortcuts import render, reverse
import traceback, os
from hello.form import UserForm

class UserListView(View):
    pass

class UserAddView(View):
    pass

class UserDelView(View):
    pass

class UserModView(View):
    pass

class UserFormView(TemplateView, View):
    template_name = 'hello/test.html'

    def post(self, request):
        # print(request.POST)
        form = UserForm(request.POST, request.FILES)
        print("已进行表单验证")
        if form.is_valid():
            print("表单验证通过")
            print(form.cleaned_data)
            file = form.cleaned_data['file']
            if file:
                with open(os.path.join('hello/upload', file.name), 'wb') as f:
                    for line in file.chunks():
                        f.write(line)
        else:
            print('表单验证不通过')
        return render(request, self.template_name, {'form': form})
