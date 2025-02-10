from flask import Flask, jsonify
from scheduler import scrape_linkedin_company_posts

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "LinkedIn Scraper API"})

@app.route("/scrape", methods=["POST"])
def scrape():
    scrape_linkedin_company_posts.delay()  # Запускаем задачу Celery
    return jsonify({"status": "Scraping started!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
