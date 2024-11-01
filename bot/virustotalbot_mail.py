import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from denemeler.sinifsal import ConfigLogger

# ConfigLogger.setup_logging()

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s') 
def test_proxy(proxy):
    """Basit bir bağlantı testi ile proxy'nin çalışıp çalışmadığını kontrol eder."""
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_temp_mail(proxy):
    if not test_proxy(proxy):
        logging.error("Proxy geçerli değil veya bağlantı hatası oluştu.")
        return None

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://email-fake.com/")

        # Sayfanın yüklenmesini bekle ve doğru XPath ile e-posta adresini al
        wait = WebDriverWait(driver, 10)
        email_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email_ch_text"]')))
        temp_mail = email_element.text
        logging.info(f"Temp-mail created: {temp_mail}")

        driver.quit()
        return temp_mail
    except Exception as e:
        logging.error(f"Failed to get temp-mail: {e}")
        if 'driver' in locals():
            driver.quit()
        return None
