from celery import Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

from celerypy import celery_app 

@celery_app.task
def scrape_linkedin_company_posts():
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.linkedin.com/company/kalyna-group/")

        # Закрываем окно авторизации (если есть)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.contextual-sign-in-modal__modal-dismiss"))
            )
            dismiss_button = driver.find_element(By.CSS_SELECTOR, "button.contextual-sign-in-modal__modal-dismiss")
            dismiss_button.click()
        except:
            pass

        # Ожидание загрузки постов
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.main-feed-activity-card"))
        )

        posts = driver.find_elements(By.CSS_SELECTOR, "article.main-feed-activity-card")

        extracted_data = []

        for post in posts:
            try:
                content_element = post.find_element(By.CSS_SELECTOR, "p.attributed-text-segment-list__content")
                content = content_element.text
            except:
                content = None

            images = []
            try:
                image_elements = post.find_elements(By.CSS_SELECTOR, "ul.feed-images-content img")
                for img in image_elements:
                    img_url = img.get_attribute('src')
                    if img_url:
                        images.append(img_url)
            except:
                pass

            extracted_data.append({
                "content": content,
                "images": images
            })

        with open("linkedin_posts.json", "w", encoding="utf-8") as json_file:
            json.dump(extracted_data, json_file, indent=4)

        return {"message": "Scraping completed!", "data": extracted_data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
