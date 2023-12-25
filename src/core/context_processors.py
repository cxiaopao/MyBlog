from .models import *
from django.db.models import Count


def post_context(request):
    """日志全局共享数据"""
    return {
        "CATEGORIES": Category.objects.values('id', 'name').annotate(Count('posts')),
        "LATEST_POSTS": Post.published.all()[:5],
        "CHOSE_POSTS": Post.published.filter(flag=True).all()[:5],
    }