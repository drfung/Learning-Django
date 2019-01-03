from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify
# Create your models here.
class ArticleColumn(models.Model):
    user = models.ForeignKey(to=User, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column

class ArticlePost(models.Model):
    author = models.ForeignKey(to=User, related_name='article')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,related_name='article_column')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(to=User, related_name="articles_like", blank=True)

    class Meta:
        ordering = ("title",)
        index_together = (('id','slug'))  # 对这两个字段建立索引

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 重写save方法,使用awesome slugify而不是django自带的slugify,以支持中文
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args, **kwargs)

    def get_absolute_url(self):
        '''
        获取对象的url
        :return:
        '''
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])
