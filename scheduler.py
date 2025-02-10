from celery.schedules import crontab
from celerypy import celery_app
from tasks import scrape_linkedin_company_posts

# Запускаем задачу каждые 6 часов
celery_app.conf.beat_schedule = {
    "scrape_every_6_hours": {
        "task": "tasks.scrape_linkedin_company_posts",
        "schedule": crontab(minute=0, hour="*/6"),  # Каждые 6 часов
    }
}

celery_app.conf.timezone = "UTC"
