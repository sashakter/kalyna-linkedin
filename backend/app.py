from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

app = Flask(__name__)

def scrape_linkedin_company_posts():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    extracted_data = []

    try:
        driver.get("https://www.linkedin.com/company/kalyna-group/")

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.contextual-sign-in-modal__modal-dismiss"))
            ).click()
        except:
            print("Модальное окно входа не появилось.")

        # Ждем загрузки постов
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.main-feed-activity-card"))
        )

        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        posts = driver.find_elements(By.CSS_SELECTOR, "article.main-feed-activity-card")

        for post in posts:
            try:
                content_element = post.find_element(By.CSS_SELECTOR, "p.attributed-text-segment-list__content")
                content = content_element.text.strip()
            except:
                content = None

            images = []
            try:
                WebDriverWait(post, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.feed-images-content img"))
                )
                image_elements = post.find_elements(By.CSS_SELECTOR, "ul.feed-images-content img")
                for img in image_elements:
                    img_url = img.get_attribute('src')
                    if img_url:
                        images.append(img_url)
            except Exception as e:
                print(f"Ошибка при извлечении изображений: {e}")

            extracted_data.append({
                "content": content,
                "images": images
            })

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

    return extracted_data

@app.route('/linkedin-posts', methods=['GET'])
def get_linkedin_posts():
    posts = scrape_linkedin_company_posts()
    return jsonify(posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
