from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
#博客类型的模型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    #显示博客类型
    def __str__(self):
        return self.type_name

#博客主体的模型
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog:{}>'.format(self.title)

    #按博客创建时间倒序排列
    class Meta:
        ordering = ['-created_time']



    