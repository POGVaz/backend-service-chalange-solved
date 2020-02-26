from .celery import app as celery_app

# Allow celery tasks to be called in the Django apps:
__all__ = ['celery_app']
