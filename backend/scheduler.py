from celery import Celery
import time

celery_app = Celery(
    "scheduler",
    broker="redis://red-XXXXXXXXXX.render.com:6379/0",  # Render Redis URL
    backend="redis://red-XXXXXXXXXX.render.com:6379/0"
)

@celery_app.task
def scrape_linkedin_company_posts():
    time.sleep(5)  # Симуляция работы
    print("✅ Данные из LinkedIn собраны!")
    return "Scraping done!"
