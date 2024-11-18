import os
import sys
import logging
import random
import string
import time
import requests
from .virustotalbot_mail import get_temp_mail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from denemeler.sinifsal import ConfigLogger
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from twocaptcha import TwoCaptcha

API_KEY = "db51f06614c7f33511fdf0f89428ea24"

ConfigLogger.setup_logging()


def generate_random_credentials():
    first_name = "".join(random.choices(string.ascii_uppercase, k=5))
    last_name = "".join(random.choices(string.ascii_uppercase, k=5))
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = "".join(
        [
            random.choice(string.ascii_letters),
            random.choice(string.digits),
            random.choice(string.punctuation),
            "".join(
                random.choices(
                    string.ascii_letters + string.digits + string.punctuation, k=9
                )
            ),
        ]
    )
    logging.info(
        f"Generated credentials - First Name: {first_name}, Last Name: {last_name}, Username: {username}, Password: {password}"
    )
    return first_name, last_name, username, password


def pazubandi(proxy):
    logging.info("Kayıt işlemine başlıyorum.")

    first_name, last_name, username, password = generate_random_credentials()
    email = get_temp_mail(proxy)
    if not email:
        logging.error("E-posta alınamadı, kayıt işlemi iptal ediliyor.")
        return
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(
        "/vagrant/buster_captcha_solver_for_humans.crx"
    )  # Buster eklentisinin .crx dosyasının tam yolunu buraya girin
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.virustotal.com/gui/join-us")
    logging.info("VirusTotal kayıt sayfasına gidildi.")
    time.sleep(10)



######################################333
    try:
            logging.info("2Captcha çözüm işlemi başlatılıyor.")
            solver = TwoCaptcha(API_KEY)

            # reCAPTCHA çözüm işlemi
            try:
                result = solver.recaptcha(
                    sitekey="6Ldjgd0kAAAAAITm7ipWF7o7kPL_81SaSfdINiOc",  # reCAPTCHA site anahtarı
                    url='https://2captcha.com/demo/recaptcha-v3',
                    version='v3',
                    action='register',
                    score='0.9'
                )

                # reCAPTCHA çözüm kodunu al
                g_recaptcha_response = result.get("code")
                if not g_recaptcha_response:
                    logging.error("reCAPTCHA kodu alınamadı.")
                    raise Exception("reCAPTCHA çözümü başarısız.")
                logging.info(f"Alınan reCAPTCHA kodu: {g_recaptcha_response}")

            except Exception as e:
                logging.error(f"2Captcha çözümü sırasında hata oluştu: {e}")
                raise e

            # Form doldurma işlemi
            try:
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]'))).send_keys(first_name)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lastName"]'))).send_keys(last_name)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(email)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userId"]'))).send_keys(username)

                password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
                password_field.send_keys(password)
                logging.info("Form bilgileri başarıyla dolduruldu.")
                time.sleep(0.5)

                password_repeat_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwordRepeat"]')))
                password_repeat_field.send_keys(password)

                tos_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tosCheckbox"]')))
                driver.execute_script("arguments[0].scrollIntoView(true);", tos_checkbox)
                time.sleep(0.5)
                tos_checkbox.click()
                logging.info("Terms of Service kutucuğu işaretlendi.")

                # reCAPTCHA iframe'ine geçiş yap
                captcha_iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'recaptcha')]")))
                driver.switch_to.frame(captcha_iframe)
                logging.info("reCAPTCHA iframe'ine geçildi.")

                # reCAPTCHA çözümünü forma ekle
                driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
                driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{g_recaptcha_response}';")
                logging.info("reCAPTCHA çözümü forma başarıyla eklendi.")

                # Ana çerçeveye geri dön
                driver.switch_to.default_content()

                # "Join us" butonuna tıkla
                time.sleep(7000)
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]')))
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", submit_button)
                logging.info("Kayıt butonuna tıklandı.")

                # Başarı kontrolü
                time.sleep(5)
                page_source = driver.page_source

                if "Signed up successfully" in page_source:
                    logging.info("Kayıt işlemi başarılı!")
                    driver.save_screenshot("success_screenshot.png")
                else:
                    logging.error("Kayıt işlemi başarısız oldu.")
                    driver.save_screenshot("error_screenshot.png")

            except Exception as e:
                logging.error(f"Form doldurma veya gönderimi sırasında hata oluştu: {e}")
                driver.save_screenshot("error_screenshot_full.png")

    except Exception as main_error:
            logging.error(f"Bir hata oluştu: {main_error}")
    finally:
            # Tarayıcıyı kapatma işlemi
            logging.info("Tarayıcı kapatılıyor.")
            driver.quit()
