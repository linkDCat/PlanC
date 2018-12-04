from django.db import models
# Create your models here.
class cms_NewsCatagory(models.Model,):
    name = models.CharField(max_length=100)

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    catagory = models.ForeignKey('cms_NewsCatagory',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('catauth.Front_User',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-pub_time']

class Comment(models.Model):
    content = models.TextField(max_length=500)
    author = models.ForeignKey('catauth.Front_User',on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey("News",on_delete=models.CASCADE,related_name='comments')

    class Meta:
        ordering = ['-pub_time']

