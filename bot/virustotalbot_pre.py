import os
from pyvirtualdisplay import Display
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from denemeler.sinifsal import ConfigLogger
import time

ConfigLogger.setup_logging()

# Buster eklentisi URL'si ve dosya yolu
BUSTER_CRX_URL = "https://clients2.googleusercontent.com/crx/blobs/AYA8VyxEiP6QUxtESKBqDwyJocAveA3nOpTEfTQd4Is80TdyKuDKdO6QWrJ8MC2QcE9rYVoHcIXauZyjlNeE7j3EJ4Z93VgK75un1s8iMgu4hJNWZX9QBstVuJMssWEUnkwAxlKa5SaPc_j8w0lrCZKpwMUuwA9V0mef/MPBJKEJCLGFGADIEMMEFGEBJFOOFLFHL_3_1_0_0.crx"
BUSTER_PATH = "/vagrant/buster_captcha_solver_for_humans.crx"

# Buster eklentisini indir
def download_buster_extension():
    try:
        logging.info("Buster eklentisi indiriliyor...")
        response = requests.get(BUSTER_CRX_URL, stream=True)
        if response.status_code == 200:
            with open(BUSTER_PATH, 'wb') as f:
                f.write(response.content)
            logging.info("Buster eklentisi başarıyla indirildi.")
            return True
        else:
            logging.error(f"Buster eklentisi indirilemedi. Status Code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Buster eklentisi indirme hatası: {e}")
        return False

# Tarayıcıyı başlatma ve Buster eklentisinin yüklendiğini doğrulama
def start_chrome():
    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        
        chrome_options = Options()
        chrome_options.add_extension(BUSTER_PATH)  # Eklentiyi ekleme
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Chrome(options=chrome_options)
        logging.info("Chrome tarayıcısı başarıyla başlatıldı.")

        # Eklentinin gerçekten yüklendiğini doğrulama
        driver.get("chrome://extensions/")
        time.sleep(2)  # Sayfanın yüklenmesini bekle
        is_buster_loaded = driver.execute_script(
            "return document.body.innerText.includes('Buster')"
        )
        
        if is_buster_loaded:
            logging.info("Buster eklentisi başarıyla yüklendi ve aktif.")
        else:
            logging.warning("Buster eklentisi yüklenemedi veya aktif değil. CAPTCHA çözümleri başarısız olabilir.")
        
        return driver, display
    except Exception as e:
        logging.error(f"Tarayıcı başlatılamadı: {e}")
        return None, None

# Ana işlev
def main():
    # 1. Buster eklentisini indir
    if not download_buster_extension():
        logging.error("Buster eklentisi indirilemedi, işlem durduruluyor.")
        exit()

    # 2. Tarayıcı başlat ve Buster eklentisini doğrula
    driver, display = start_chrome()
    if driver:
        logging.info("Tarayıcı ve Buster eklentisi doğrulandı, işlemler devam edebilir.")
        driver.quit()
        display.stop()
    else:
        logging.error("Tarayıcı başlatılamadı veya Buster eklentisi yüklenemedi.")

if __name__ == "__main__":
    main()
