from django.contrib import admin
from article.models import Beauty


# Register your models here.
class BeautyModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'score', 'title', 'author', 'date', 'url')
    search_fields = ('title',)
    ordering = ('date',)


admin.site.register(Beauty, BeautyModelAdmin)