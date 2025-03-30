from __future__ import absolute_import, unicode_literals

# 讓 Django 確保 Celery 被載入
from .celery import app as celery_app

__all__ = ("celery_app",)