from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # 確保只在主進程執行
            # import core.tasks

            # import core.sentiment_analyzer
            # core.sentiment_analyzer.sentiment_analyzer()

            # import core.tokenizer
            # core.tokenizer.tokenizer()
            # core.tokenizer.test()

            # import core.news_scraper
            # core.news_scraper.news_collector()

            # import core.utils
            # core.utils.set_news_categories()

            # import core.models as models
            # print(models.analysed_news.db_newsCount())
            ...
