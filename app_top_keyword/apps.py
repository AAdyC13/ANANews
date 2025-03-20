from django.apps import AppConfig
import os

class AppTopKeywordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_top_keyword'
    
    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # 確保只在主進程執行
            ...
            # import app_top_keyword.top_keyword_ana
            # app_top_keyword.top_keyword_ana.top_keyword_ana()