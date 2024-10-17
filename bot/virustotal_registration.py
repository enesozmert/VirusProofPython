import logging
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Rastgele kullanıcı adı ve şifre oluşturma
def generate_random_credentials():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    logging.info(f"Generated credentials - Username: {username}, Password: {password}")
    return username, password

# Selenium ile proxy ve tarayıcı ayarları
def start_browser_with_proxy(proxy):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')  # Proxy ekle

    # CAPTCHA çözen Buster eklentisini yüklemek için .crx dosyasının yolunu ekleyin
    chrome_options.add_extension("/path/to/buster_extension.crx")

    # Brave veya Chrome tarayıcısı için ayarlar
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    # WebDriver ile tarayıcıyı başlat
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    logging.info(f"Browser started with proxy: {proxy}")
    return driver

# VirusTotal kaydolma işlemi
def register_virustotal(driver, email, username, password):
    driver.get("https://www.virustotal.com/gui/join-us")
    logging.info("VirusTotal registration page opened.")

    # Formu doldur
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email)

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    # CAPTCHA çözen Buster eklentisini kullanarak CAPTCHA'yi çöz
    try:
        buster_button = driver.find_element(By.XPATH, "//*[contains(@class, 'buster-captcha-solver')]")
        buster_button.click()
        logging.info("CAPTCHA solving initiated using Buster.")
        time.sleep(10)  # CAPTCHA'nın çözülmesi için biraz bekleyelim
    except Exception as e:
        logging.error(f"CAPTCHA solving failed: {e}")

    # Formu gönder
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    # İşlemin sonucunu bekle ve logla
    time.sleep(10)  # İşlemin tamamlanması için bekle
    if "successful_registration_token" in driver.page_source:
        logging.info("Successfully registered on VirusTotal.")
    else:
        logging.error("Registration failed.")
    
    driver.quit()

def main():
    # Proxy ve kullanıcı bilgilerini ayarla
    proxy = "http://178.48.68.61:18080"
    email = "example@mail.com"
    username, password = generate_random_credentials()

    # Tarayıcıyı başlat
    driver = start_browser_with_proxy(proxy)
    register_virustotal(driver, email, username, password)

if __name__ == "__main__":
    main()
