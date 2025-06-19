# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Конфигурация (ПРОВЕРЬТЕ ПУТИ!)
YANDEX_BROWSER_PATH = r'C:\Users\hitma\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'
YANDEX_DRIVER_PATH = 'yandexdriver.exe'  # Файл должен быть в папке со скриптом
WB_URL = "https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki"
OUTPUT_FILE = "wildberries_products.xlsx"

def setup_driver():
    """Настройка драйвера"""
    if not os.path.exists(YANDEX_DRIVER_PATH):
        print(f"Ошибка: Файл драйвера '{YANDEX_DRIVER_PATH}' не найден")
        print("Скачайте с https://yandex.ru/dev/yandexdriver/")
        return None

    options = Options()
    options.binary_location = YANDEX_BROWSER_PATH
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        service = Service(executable_path=YANDEX_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Ошибка запуска драйвера: {str(e)}")
        return None

def main():
    print("Запуск парсера Wildberries...")
    driver = setup_driver()
    if not driver:
        return

    try:
        driver.get(WB_URL)
        time.sleep(3)
        
        # Прокрутка и парсинг
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(1.5)
        
        products = []
        cards = driver.find_elements(By.CSS_SELECTOR, "div.product-card__wrapper")
        
        for card in cards:
            try:
                products.append({
                    "Название": card.find_element(By.CSS_SELECTOR, "span.product-card__name").text,
                    "Цена": card.find_element(By.CSS_SELECTOR, "ins.price__lower-price").text.replace("₽", "").strip(),
                    "Ссылка": card.find_element(By.CSS_SELECTOR, "a.product-card__link").get_attribute("href")
                })
            except:
                continue

        if products:
            pd.DataFrame(products).to_excel(OUTPUT_FILE, index=False)
            print(f"Данные сохранены в {OUTPUT_FILE}")
            
    finally:
        driver.quit()

if __name__== "__main__":
    main()