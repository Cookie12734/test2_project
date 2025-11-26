from django.contrib import admin

from .models import Category, Test2News
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title')
    
    list_display_links = ('id', 'title')

class PhotoPostAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title')
    
    list_display_links = ('id', 'title')
    
        #管理サイトに登録
admin.site.register(Category, CategoryAdmin)

admin.site.register(Test2News, PhotoPostAdmin)
