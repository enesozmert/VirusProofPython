from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# LOG AYARI
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Tarayıcıyı global bir değişkende sakla
persistent_driver = None

def get_temp_mail(proxy=None):
    global persistent_driver  # driver'ı global bir değişkende sakla
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        # Tarayıcıyı yalnızca ilk çağrıda başlat
        if not persistent_driver:
            service = Service("/usr/local/bin/chromedriver")
            persistent_driver = webdriver.Chrome(options=options, service=service)
        
        persistent_driver.get("https://email-fake.com/")

        # Sayfanın yüklenmesini bekle ve e-posta adresini al
        wait = WebDriverWait(persistent_driver, 10)
        email_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email_ch_text"]'))
        )
        temp_mail = email_element.text
        logging.info(f"Temp-mail created: {temp_mail}")

        # Tarayıcıyı açık tutmak için driver'ı kapatma
        return temp_mail
    except Exception as e:
        logging.error(f"Failed to get temp-mail: {e}")
        return None
