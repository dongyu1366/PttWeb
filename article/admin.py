from django.contrib import admin
from article.models import Beauty


class BeautyModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'score', 'title', 'author', 'date', 'url')
    search_fields = ('title',)
    ordering = ('date',)


# Register your models here.
admin.site.register(Beauty, BeautyModelAdmin)