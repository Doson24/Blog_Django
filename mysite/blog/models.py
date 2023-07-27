from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class HUI(models.Model):
    pass


class Post(models.Model):
    """
    slug - короткая метка поста, соержит только буквы, цифры, знаки
    подчеркивания или дефисы.
    (Для формирования дружественной поисковой оптимизации адресов)
    """

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title


"""
>>> from blog.models import Post
>>> user = User.objects.get(username='admin')  
>>> post = Post(title='Ana',
... slug='ana',
... body='qwerty',
... author=user)
>>> post.save
>>> Post.objects.all()
<QuerySet [<Post: Ana>, <Post: What do you do?>, <Post: Test>, <Post: Тестт>]>
>>> Post.objects.filter(publish__year=2023) 
<QuerySet [<Post: Ana>, <Post: What do you do?>, <Post: Test>, <Post: Тестт>]>
>>> Post.objects.filter(publish__year=2023, author__username='admin') 
<QuerySet [<Post: Ana>, <Post: What do you do?>, <Post: Test>, <Post: Тестт>]>
>>> Post.objects.filter(publish__year=2023, author__username='admin').exclude(title__startswith='Ana') 
<QuerySet [<Post: What do you do?>, <Post: Test>, <Post: Тестт>]>
>>> post.delete()
(1, {'blog.Post': 1})
>>> Post.objects.all()                                                                                 
<QuerySet [<Post: What do you do?>, <Post: Test>, <Post: Тестт>]>

>>> Post.published.filter(title__startswith='A')   
<QuerySet [<Post: Ana>]>

"""
