from django import forms
from django.core import validators

from .models import Comment


# class CommentForm(forms.Form):
#     """手动申明表单"""
#     name = forms.CharField(max_length=50, label='姓名',
#                            validators=[validators.MinValueValidator(2, "姓名长度必须大于2")], required=True)
#     body = forms.CharField(label='正文', required=True)


class CommentForm(forms.ModelForm):
    """根据数据模型生成表单"""

    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "mb-2 border rounded-md p-2 text-sm",
                "placeholder": "请输入用户名"
            }),
            "body": forms.Textarea(attrs={
                "placeholder": "请留下你的评论",
                "class": "w-full border rounded-md p-2 text-sm",
                "cols": 30,
                "rows": 3,
            })
        }
