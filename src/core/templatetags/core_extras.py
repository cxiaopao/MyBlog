from django import template
from django.db.models import Count
from taggit.models import Tag

from ..models import Post

register = template.Library()


# 自定义to_str过滤器
@register.filter(name='to_str')
def to_str(value):
    return str(value)


# 自定义“包含标签”页面
@register.inclusion_tag('segment/tags.html')
def display_tags():
    tags = Tag.objects.all()
    return {
        "tags": tags
    }


@register.inclusion_tag('segment/popular-posts.html')
def display_popular_posts(count=5):
    popular_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {
        "popular_posts": popular_posts
    }


@register.filter(name='highlight')
def highlight(text, search):
    if search:
        text = text.replace(search, f'<span class="bg-secondary text-white">{search}</span>')
    return text
