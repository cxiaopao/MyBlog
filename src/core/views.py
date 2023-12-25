from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from taggit.models import Tag
from .forms import CommentForm
from .models import Profile, Category, Post, Comment, Slide


# Create your views here.
def index(request):
    # items = Post.objects.filter(status='published')[:10]
    items = Post.published.all()[:10]
    slides = Slide.objects.all()
    return render(request, 'index.html', {
        "items": items,
        "slides": slides
    })


def about(request):
    item = Profile.objects.get(id=1)
    item.hits += 1
    item.save()
    return render(request, 'about.html', {"item": item})


def posts(request):
    # items = Post.objects.filter(status='published')
    items = Post.published.all()
    # 按标签分类，过滤
    tag = request.GET.get('tag', None)
    if tag:
        tag_obj = Tag.objects.get(slug=tag)
        items = items.filter(tags__in=[tag_obj])  # tag_obj in tags

    category = request.GET.get('category', None)
    if category:
        items = items.filter(category_id=category)

    paginator = Paginator(items, per_page=10)  # 分页器
    page = request.GET.get('page')  # 页码
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'post-list.html', {
        "items": items,
    })


def details(request, slug):
    item = Post.objects.get(slug=slug)
    # tags = item.tags.split(',')
    try:
        prev_post = item.get_next_by_created_time()
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = item.get_previous_by_created_time()
    except Post.DoesNotExist:
        next_post = None

    comments = Comment.objects.filter(post=item, active=True)
    item.filtered_comments = comments

    form = CommentForm()

    if request.method == 'POST':
        # name = request.POST.get('name', None)
        # body = request.POST.get('body', None)
        # if name and body:
        #     comment = Comment()
        #     comment.name = name
        #     comment.body = body
        #     comment.post = item
        #     comment.ip = get_ip(request)
        #     comment.save()
        # else:
        #     return HttpResponse('请输入必要信息')
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = item
            comment.ip = get_ip(request)
            comment.save()
        return redirect(item.get_post_url())

    return render(request, "details.html", {
        "item": item,
        "prev_post": prev_post,
        "next_post": next_post,
        "form": form,
    })


def get_ip(request):
    """获取请求者的IP信息"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def search_posts(request):
    items = Post.published.all()
    q = request.GET.get('q', None)
    if q.strip():
        items = items.filter(title__contains=q)
    else:
        return redirect(reverse('posts'))
    paginator = Paginator(items, per_page=5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'search-posts.html', {
        "items": items,
    })
