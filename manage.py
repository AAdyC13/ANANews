#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# celery -A ANANews worker -l  info -P eventlet
# daphne -b 127.0.0.3 -p 8001 ANANews.asgi:application


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANANews.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) == 1 or sys.argv[1] == "runserver":
        sys.argv = ["manage.py", "runserver", "127.0.0.3:8000"]
        # sys.argv = ["manage.py", "runserver", "0.0.0.0:8000"]
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
