from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")

app = Celery("backend")

# Use Redis as broker
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

# Optional: auto-discover tasks
app.autodiscover_tasks()

