import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from .virustotalbot_kayit import pazubandi

# LOG AYARI
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def setup_chrome_driver():
    try:
        chrome_options = webdriver.ChromeOptions()
        
        # Eklentinin indirilmiş .crx dosyasını ekle
        chrome_options.add_extension("/vagrant/buster_captcha_solver_for_humans.crx")  # Buster eklentisinin .crx dosyasının tam yolunu buraya girin
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")

        logging.info("Chrome tarayıcısı başlatılmaya çalışılıyor...")
        # `Service` nesnesi ile belirtilen chromedriver yolunu kullanarak başlat
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Chrome tarayıcısı başarıyla başlatıldı.")
        return driver
    except Exception as e:
        logging.error(f"Chrome tarayıcısı başlatılamadı: {e}")
        return None

def is_buster_installed(driver):
    try:
        # Buster eklentisinin options sayfasına git
        driver.get("chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html")
        time.sleep(3)  # Sayfanın yüklenmesini bekle

        # Eğer sayfa açılabilirse, eklenti yüklüdür
        if "Buster" in driver.title:
            logging.info("Buster eklentisi mevcut.")
            return True
        else:
            logging.error("Buster eklentisi yüklü değil.")
            return False
    except Exception as e:
        logging.error(f"Buster eklentisinin varlığı doğrulanamadı: {e}")
        return False




def main(proxy):
    driver = setup_chrome_driver()
    if driver:
        if is_buster_installed(driver):
            logging.info("Buster eklentisi mevcut, işlemler devam edebilir.")
            driver.quit()
            pazubandi(proxy)  # Bu aşamada gerekli işlevi çağırın
        else:
            logging.error("Buster eklentisi yüklü değil.")
        driver.quit()
    else:
        logging.error("Tarayıcı başlatılamadı.")

if __name__ == "__main__":
    main()
