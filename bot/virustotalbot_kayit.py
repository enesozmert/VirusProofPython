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
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains


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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension("/vagrant/buster_captcha_solver_for_humans.crx")  # Buster eklentisinin .crx dosyasının tam yolunu buraya girin
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    #chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled");
    driver = webdriver.Chrome(options=chrome_options)
    
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.virustotal.com/gui/join-us")
    logging.info("VirusTotal kayıt sayfasına gidildi.")
    time.sleep(10)
    
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]'))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lastName"]'))).send_keys(last_name)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userId"]'))).send_keys(username)
        
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.send_keys(password)
        
        logging.info("Buraya geldi")
        logging.warning("SSL certificate error")

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
        time.sleep(2)
        
# CAPTCHA manuel kontrol ve tıklama işlemi
#
# ***************

        try:
            # İlk CAPTCHA iframe'ine geçiş
            captcha_iframe = WebDriverWait(driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
            )

            # Checkbox'a tıklama
            recaptcha_checkbox = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']/div"))
            )
            recaptcha_checkbox.click()
            logging.info("reCAPTCHA kutucuğuna başarıyla tıklandı.")
            driver.switch_to.default_content()
            time.sleep(5)

            # İkinci (challenge) iframe'e geçiş
            challenge_iframe = WebDriverWait(driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']"))
            )
        
            # Shadow DOM içindeki butona erişim ve tıklama için JavaScript
            solver_button_status = driver.execute_script("""
                // İlk olarak shadow host'u seçin
                let shadowHost = document.querySelector("div.button-holder.help-button-holder");
                
                // Shadow root'a erişim
                if (shadowHost && shadowHost.shadowRoot) {
                    let solverButton = shadowHost.shadowRoot.querySelector("#solver-button");
                    if (solverButton) {
                        solverButton.click();
                        return "Button clicked";
                    } else {
                        return "Button not found";
                    }
                } else {
                    return "Shadow host not found";
                }
            """)

            if solver_button_status == "Button clicked":
                logging.info("Solver butonuna başarıyla tıklandı.")
            else:
                logging.error(f"Solver butonuna erişim başarısız: {solver_button_status}")
            time.sleep(7)

        except Exception as e:
            logging.error(f"Elemente tıklanırken bir hata oluştu: {e}")



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
        time.sleep(100)
        driver.quit()