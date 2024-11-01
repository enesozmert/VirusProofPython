import logging
import random
import string
import time
from .virustotalbot_mail import get_temp_mail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from denemeler.sinifsal import ConfigLogger

ConfigLogger.setup_logging()

def generate_random_credentials():
    first_name = ''.join(random.choices(string.ascii_uppercase, k=5))
    last_name = ''.join(random.choices(string.ascii_uppercase, k=5))
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = ''.join([
        random.choice(string.ascii_letters),
        random.choice(string.digits),
        random.choice(string.punctuation),
        ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=9))
    ])
    logging.info(f"Generated credentials - First Name: {first_name}, Last Name: {last_name}, Username: {username}, Password: {password}")
    return first_name, last_name, username, password

def pazubandi(proxy):
    logging.info("Kayıt işlemine başlıyorum.")
    
    first_name, last_name, username, password = generate_random_credentials()
    email = get_temp_mail(proxy)
    if not email:
        logging.error("E-posta alınamadı, kayıt işlemi iptal ediliyor.")
        return
    
    options = webdriver.ChromeOptions()
    options.add_extension('/vagrant/buster_captcha_solver_for_humans.crx')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.virustotal.com/gui/join-us")
    logging.info("VirusTotal kayıt sayfasına gidildi.")
    
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]'))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lastName"]'))).send_keys(last_name)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userId"]'))).send_keys(username)
        
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.send_keys(password)
        
        time.sleep(0.5)
        
        password_repeat_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwordRepeat"]')))
        password_repeat_field.send_keys(password)

        tos_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tosCheckbox"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", tos_checkbox)
        time.sleep(0.5)
        tos_checkbox.click()
        logging.info("Terms of Service kutucuğu işaretlendi.")
        
        # "Join us" butonuna tıkla
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_button)
        logging.info("Kayıt butonuna tıklandı.")
        
        # 4 saniye bekle ve CAPTCHA alanını kontrol et
        time.sleep(4)
        
        # CAPTCHA manuel kontrol ve tıklama işlemi
        try:
            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", recaptcha_checkbox)
            recaptcha_checkbox.click()
            logging.info("CAPTCHA kutucuğu manuel olarak işaretlendi.")
            time.sleep(5)  # CAPTCHA çözümü için kısa bekleme süresi
        except Exception as e:
            logging.warning(f"CAPTCHA işaretlenemedi: {e}")
            driver.save_screenshot("/vagrant/captcha_click_failed.png")
            logging.error("CAPTCHA kutucuğu işaretlenemedi, işlem sonlandırılıyor.")
            return

        # Başarı durumunu kontrol et ve ekran görüntüsü al
        time.sleep(3)
        new_url = driver.current_url
        if "dashboard" in new_url or "signed up successfully" in driver.page_source:
            logging.info("Kayıt başarılı, ekran görüntüsü alınıyor.")
            driver.save_screenshot("/vagrant/success_screenshot.png")
        else:
            logging.error("Üyelik başarısız oldu, ekran görüntüsü alınıyor.")
            driver.save_screenshot("/vagrant/error_screenshot.png")
    except Exception as e:
        logging.error(f"Kayıt işlemi sırasında hata oluştu: {e}")
        driver.save_screenshot("/vagrant/error_screenshot_full.png")
        logging.info("Ekran görüntüsü '/vagrant/error_screenshot_full.png' olarak kaydedildi.")
    finally:
        driver.quit()
