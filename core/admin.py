from django.contrib import admin
from .models import analysed_news
from .models import system_config
# Register your models here.


@admin.register(analysed_news)
class analysed_news(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'news_id_one',
                    'news_id_two', 'content', 'photo_link')  # 在後台顯示的欄位

    search_fields = ('news_id_one', 'news_id_two', 'date',
                     'category', 'title')  # 可搜尋的欄位


@admin.register(system_config)
class system_config(admin.ModelAdmin):
    list_display = (
        'sysdb_id', 'sysdb_name', 'sysdb_data'
    )  # 在後台顯示的欄位
    search_fields = ('sysdb_id', 'sysdb_name')  # 可搜尋的欄位
