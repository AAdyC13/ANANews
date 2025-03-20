from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # 確保只在主進程執行
            ...
            # import core.tokenizer
            # core.tokenizer.tokenizer()
            
            # import core.news_scraper
            # core.news_scraper.news_scraper()
            