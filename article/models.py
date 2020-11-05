from django.db import models


class Beauty(models.Model):
    source_token = models.IntegerField()
    category = models.CharField(max_length=50)
    score = models.IntegerField()
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    date = models.DateTimeField()
    url = models.CharField(max_length=200)
    images_amounts = models.IntegerField()
    images = models.CharField(max_length=5000, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
