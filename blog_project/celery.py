from celery import Celery

app = Celery('blog_project')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

app.conf.update(
    broker_url='redis://0.0.0.0:6379/0',
    broker_transport_options={'visibility_timeout': 3600},
    result_backend='redis://0.0.0.0:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Kyiv',
    enable_utc=True,
)
