from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True,blank=True,upload_to='Files')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="blog_posts")

    def total_like(self):
        return self.like.count()

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)       

    def __str__(self):
        return '%s - %s' % (self.post.title,self.author)