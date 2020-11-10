# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
