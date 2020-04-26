import re
from django import forms
from hello.models import Project_User


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = Project_User
        fields = "__all__"

    def clean_name(self):
        pass

    def clean_password(self):
        pass

    def clean_phone(self):
        pass

    def clean_age(self):
        pass

    def clean_sex(self):
        pass

class UserModefyForm(forms.ModelForm):
    class Meta:
        model = Project_User
        fields = "__all__"

    def clean_name(self):
        pass

    def clean_password(self):
        pass

    def clean_phone(self):
        pass

    def clean_age(self):
        pass

    def clean_sex(self):
        pass


