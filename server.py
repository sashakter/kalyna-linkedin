from fastapi import FastAPI
import json
import os
from tasks import scrape_linkedin_company_posts

app = FastAPI()

JSON_FILE = "linkedin_posts.json"

@app.get("/linkedin_posts")
def get_linkedin_posts():
    if not os.path.exists(JSON_FILE):
        return {"error": "Файл не найден. Запустите скрапинг вручную."}

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return {"posts": data}

@app.post("/scrape")
def run_scraping():
    scrape_linkedin_company_posts.delay()  # Запускаем фоновую задачу
    return {"message": "Скрапинг запущен в фоне!"}
