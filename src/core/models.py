from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse


# Create your models here
class Profile(models.Model):
    """个体资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="用户")
    fullname = models.CharField("全名", max_length=20, blank=True)
    title = models.CharField("头衔", max_length=120, blank=True)
    avatar = models.ImageField("头像", default="avatars/avatar.png", upload_to="avatars")
    phone = models.CharField("手机", max_length=50, blank=True)
    wechat = models.CharField("微信", max_length=50, blank=True)
    qq = models.CharField("QQ", max_length=50, blank=True)
    url = models.URLField("网站", max_length=250, blank=True)
    github = models.URLField("GitHub", max_length=250, blank=True)
    bio = models.TextField("简介", blank=True)
    hits = models.IntegerField("点击", default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}的个人资料"

    class Meta:
        verbose_name = '个人资料'
        verbose_name_plural = '个人资料'
        ordering = ('-created_time',)


class Category(models.Model):
    """日志分类"""
    slug = models.SlugField('地址缩写', max_length=120)
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=250, blank=True)
    order = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-order', 'id')
        verbose_name = '日志分类'
        verbose_name_plural = '日志分类'


class PublishedManager(models.Manager):
    """自定义模型管理器"""

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """博文日志"""
    STATUS_CHOICE = (
        ('draft', '草稿'),
        ('published', '发布')
    )

    title = models.CharField('标题', max_length=250)
    slug = models.SlugField('地址缩写', max_length=120, unique_for_date='created_time')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    img = models.ImageField('图片', upload_to='uploads', blank=True, null=True)
    summary = models.CharField('摘要', max_length=250, blank=True)
    body = models.TextField('正文')
    # tags = models.CharField('标签', max_length=200)
    tags = TaggableManager('标签')
    views = models.IntegerField('浏览量', default=0)
    flag = models.BooleanField('标记', default=False)
    status = models.CharField('状态', max_length=120, choices=STATUS_CHOICE, default='draft')

    updated_time = models.DateTimeField('更新时间', auto_now=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_post_url(self):
        """获取当前日志的地址"""
        return reverse('details', args=[self.slug, ])

    # 默认管理器
    objects = models.Manager()

    # 自定义模型管理器
    published = PublishedManager()

    class Meta:
        verbose_name = '博文日志'
        verbose_name_plural = '博文日志'
        ordering = ('-created_time',)


class Comment(models.Model):
    """日志评论"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='日志评论')
    name = models.CharField('用户名', max_length=120)
    ip = models.CharField('IP', max_length=50, blank=True)
    body = models.TextField('正文')
    active = models.BooleanField('有效', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f"<{self.name}>针对<<{self.post}>>的评论"

    class Meta:
        verbose_name = '日志评论'
        verbose_name_plural = '日志评论'
        ordering = ('-created_time',)


class Slide(models.Model):
    """首页轮播图"""
    title = models.CharField('标题', max_length=120)
    sub_title = models.CharField('副标题', max_length=120, blank=True)
    description = models.TextField('描述', blank=True)
    link = models.CharField('链接', max_length=120, blank=True)
    img = models.ImageField('图片', upload_to='uploads', blank=True)
    order = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-order', 'id')
        verbose_name = '首页轮播图'
        verbose_name_plural = '首页轮播图'
