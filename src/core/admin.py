from django.contrib import admin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Profile, Category, Post, Comment, Slide


class ProfileAdminForm(forms.ModelForm):
    """个人资料管理表单"""

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'bio': SummernoteWidget()
        }


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """个人资料管理后台"""
    form = ProfileAdminForm
    list_display = ('user', 'fullname', 'title', 'phone', 'created_time')
    ordering = ('-created_time',)


class CategoryAdminForm(forms.ModelForm):
    """类别后台管理表单"""

    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": forms.Textarea
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """类别后台管理"""
    form = CategoryAdminForm
    list_display = ('slug', 'name', 'order')
    list_editable = ('order',)


class PostAdminForm(forms.ModelForm):
    """博文日志管理表单"""

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'summary': forms.Textarea,
            'body': SummernoteWidget()
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """博文日志管理后台"""
    form = PostAdminForm
    list_display = ('title', 'slug', 'category', 'views', 'flag', 'status')
    ordering = ('-created_time', 'status')
    search_fields = ('title', 'body')
    list_filter = ('category', 'flag', 'status')
    date_hierarchy = 'created_time'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """日志评论后台管理"""
    list_display = ('post', 'name', 'ip', 'active', 'created_time')
    list_filter = ('active', 'created_time')
    ordering = ('-created_time',)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'link', 'order')
    link_filed = ('title',)
    list_editable = ('order',)
    ordering = ('-order', 'id')
