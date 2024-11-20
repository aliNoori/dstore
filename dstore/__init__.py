# store/__init__.py

from __future__ import absolute_import, unicode_literals

# این کد مطمئن می‌شود که برنامه همیشه هنگام شروع Django وارد شده است
from .celery import app as celery_app

__all__ = ('celery_app',)
