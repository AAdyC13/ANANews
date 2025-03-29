from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 設定 Django 的 settings 模組
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ANANews.settings")

# 創建 Celery 實例
app = Celery("ANANews")

# 加載 Django 設定
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自動發現 Django App 內的 tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")