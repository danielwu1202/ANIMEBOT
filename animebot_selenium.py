from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def selenium_crawler():
    # 設定 user-agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    # 設定 Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')

    # 可選：隱藏自動化控制痕跡
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 可選：無頭模式
    chrome_options.add_argument("--headless")

    # 設定 WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打開目標網站
        url = "https://ani.gamer.com.tw/"  # 替換為目標網站
        driver.get(url)

        # 等待頁面加載（可根據需要調整）
        time.sleep(3)

        print(driver.page_source)

    finally:
        # 關閉瀏覽器
        driver.quit()