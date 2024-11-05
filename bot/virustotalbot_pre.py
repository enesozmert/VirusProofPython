import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from .virustotalbot_kayit import pazubandi
#LOG AYARI BU DOKUNMA
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Buster eklentisi URL'si
EXTENSION_URL = 'https://chromewebstore.google.com/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl'


#pip3 install webdriver-manager --upgrade ile webdriver sürümünü güncellemek gerekiyor.


def setup_chrome_driver():
    try:
        # Chrome ayarlarını başlat
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")  # Gerekirse headless modu ekleyin

        # ChromeDriver ile tarayıcıyı başlat
        logging.info("Chrome tarayıcısı başlatılmaya çalışılıyor...")
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("Chrome tarayıcısı başarıyla başlatıldı.")
        except Exception as e:
            logging.error(f"Chrome tarayıcısı başlatılamadı: {e}")
            return None

        return driver
    except Exception as e:
        logging.error(f"Tarayıcı ayarları yapılandırılamadı: {e}")
        return None

def install_buster_extension(driver):
    try:
        # Buster eklentisi sayfasına git
        logging.info("Buster eklentisi sayfasına gidiliyor...")
        driver.get(EXTENSION_URL)
        time.sleep(5)  # Sayfanın yüklenmesini bekleyin

        # "Chrome'a Ekle" butonunu bul ve tıkla
        try:
            add_to_chrome_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Chrome']")
            add_to_chrome_button.click()
            logging.info("'Chrome'a Ekle' butonuna tıklandı.")
            time.sleep(2)  # İşlemin başlaması için bekleyin

            # Onay penceresinde "Eklenti Ekle" butonuna basmak için
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
            logging.info("'Eklenti Ekle' onaylandı.")
            time.sleep(5)  # Eklentinin yüklenmesini bekleyin

            logging.info("Buster eklentisi başarıyla yüklendi.")
        except Exception as e:
            logging.error(f"'Chrome'a Ekle' butonuna tıklanamadı veya eklenti yüklenemedi: {e}")
            return False

        return True
    except Exception as e:
        logging.error(f"Buster eklentisi yüklenirken hata oluştu: {e}")
        return False

def main(proxy):
    driver = setup_chrome_driver()
    if driver:
        if install_buster_extension(driver):
            logging.info("Eklenti başarıyla yüklendi, işlemler devam edebilir.")
            pazubandi(proxy)
        else:
            logging.error("Eklenti yüklenemedi.")
        driver.quit()
    else:
        logging.error("Tarayıcı başlatılamadı.")

if __name__ == "__main__":
    main()
