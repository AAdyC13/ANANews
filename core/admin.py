from django.contrib import admin
from .models import analysed_news
# Register your models here.

@admin.register(analysed_news)
class analysed_news(admin.ModelAdmin):
    list_display = (
    'title','category','date','news_id_one', 'news_id_two',    'content', 
    'sentiment', 'summary', 'top_key_freq', 'tokens', 'tokens_v2', 
    'entities', 'token_pos', 'photo_link'
)  # 在後台顯示的欄位
    search_fields = ('news_id_one', 'news_id_two', 'date', 'category', 'title')  # 可搜尋的欄位