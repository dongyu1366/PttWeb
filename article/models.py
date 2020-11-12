from django.db import models


class Beauty(models.Model):
    source_token = models.IntegerField(unique=True)
    category = models.CharField(max_length=50)
    score = models.IntegerField()
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    date = models.DateTimeField()
    url = models.CharField(max_length=500)
    images_amounts = models.IntegerField()
    images = models.CharField(max_length=10000, blank=True, null=True)
    dt_created = models.DateTimeField(blank=True, null=True)
    dt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beauty'
