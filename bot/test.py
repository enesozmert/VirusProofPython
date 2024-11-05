from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

print("işleme başlangıc")
#her işlem in baslangıcı

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
logging.info("Buraya geldik")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    # search_box = driver.find_element(By.NAME, "q")
    # search_box.send_keys("Selenium WebDriver")
    # search_box.send_keys(Keys.RETURN)
    
    print("hata alınmadı chrome baslatılıyor.")
except Exception as e:
    print("hata alındı log ekrana basılıyor. ")
    logging.warning(f"Error: {e}")
    logging.info("{e}".format)

logging.debug("Google sayfası açıldı")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("CTRL+C detected, exiting...")
    driver.quit()
    exit()
driver.quit()


