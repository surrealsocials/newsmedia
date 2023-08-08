from django.db import models
from datetime import datetime
from django.utils import timezone

class NewsArticle(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    subtitle = models.TextField()
    tag = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    url = models.TextField(default='#')
    story = models.TextField(default="")
    last_update = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title