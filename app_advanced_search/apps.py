from django.apps import AppConfig
import os


class AppAdvancedSearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_advanced_search'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # 確保只在主進程執行
            ...
        # from .assoc_ana import ana_main
        # print(ana_main("美國", "and", "全部", 1))
