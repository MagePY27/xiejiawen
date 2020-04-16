from django import forms
#原生表单验证各种表单类型以及自定义

class UserForm(forms.Form):
    name = forms.CharField(max_length=12, required=True)
    phone = forms.CharField(max_length=11, required=False)
    # age = forms.IntegerField(max_value=100, required=False)
    skill = forms.CharField(max_length=10, required=False)
    file = forms.FileField()
    info = forms.CharField(max_length=100, required=True)

    #自定义验证格式， clean_字段
    """
    Django的form系统自动寻找匹配的函数方法，该方法以clean_开头，并以字段名称结束。
    如果有这样的方法，那么它将在校验时被调用， clean_info()方法将在指定字段的默认校验逻辑
    执行之后被调用。
    本例中，在必填CharField这个校验逻辑之后， 因为字段数据已被部分处理，所以它被从self.cleaned_data
    中提取出来，同样我们不必担心数据是否为空，因为它已被校验过了。
    """
    def clean_info(self):
        print(self.cleaned_data)
        info = self.cleaned_data['info']
        num_info = len(info.strip())
        print("info长度为:", num_info)
        if num_info < 4:
            raise forms.ValidationError('info too short')
        return info