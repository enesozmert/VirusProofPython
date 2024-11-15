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

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]'))
        ).send_keys(first_name)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="lastName"]'))
        ).send_keys(last_name)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
        ).send_keys(email)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="userId"]'))
        ).send_keys(username)

        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        password_field.send_keys(password)

        logging.info("Buraya geldi")
        logging.warning("SSL certificate error")

        time.sleep(0.5)

        password_repeat_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordRepeat"]'))
        )
        password_repeat_field.send_keys(password)

        tos_checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tosCheckbox"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tos_checkbox)
        time.sleep(0.5)
        tos_checkbox.click()
        logging.info("Terms of Service kutucuğu işaretlendi.")
        time.sleep(9)
        # "Join us" butonuna tıkla
        # submit_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))
        # )
        # driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        # time.sleep(1)
        # driver.execute_script("arguments[0].click();", submit_button)
        # logging.info("Kayıt butonuna tıklandı.")

        # 4 saniye bekle ve CAPTCHA alanını kontrol et
        time.sleep(7)

        # CAPTCHA manuel kontrol ve tıklama işlemi
        #
        # ***************

API_KEY = "db51f06614c7f33511fdf0f89428ea24"
WEBSITE_URL = "https://2captcha.com/demo/recaptcha-v3"
SITE_KEY = "6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu"
MIN_SCORE = 0.9
PAGE_ACTION = "test"

    # reCAPTCHA çözme görevini başlat
    def create_captcha_task():
        url = "https://api.2captcha.com/createTask"
        payload = {
            "clientKey": API_KEY,
            "task": {
                "type": "RecaptchaV3TaskProxyless",
                "websiteURL": WEBSITE_URL,
                "websiteKey": SITE_KEY,
                "minScore": MIN_SCORE,
                "pageAction": PAGE_ACTION,
                "isEnterprise": False,
                "apiDomain": "recaptcha.net"
            }
        }
        response = requests.post(url, json=payload)
        result = response.json()

        if result.get("errorId") == 0:
            task_id = result.get("taskId")
            logging.info(f"reCAPTCHA çözme görevi oluşturuldu, Task ID: {task_id}")
            return task_id
        else:
            logging.error(f"reCAPTCHA çözme görevi oluşturulamadı: {result.get('errorDescription')}")
            return None

    # Görevin tamamlanmasını ve çözümü almayı bekler
    def get_captcha_solution(task_id):
        url = "https://api.2captcha.com/getTaskResult"
        payload = {
            "clientKey": API_KEY,
            "taskId": task_id
        }

        while True:
            response = requests.post(url, json=payload)
            result = response.json()

            if result.get("errorId") == 0:
                if result.get("status") == "ready":
                    g_recaptcha_response = result["solution"]["gRecaptchaResponse"]
                    logging.info("reCAPTCHA çözümü alındı.")
                    return g_recaptcha_response
                else:
                    logging.info("reCAPTCHA çözümü bekleniyor...")
                    time.sleep(5)
            else:
                logging.error(f"reCAPTCHA çözümleme sırasında hata: {result.get('errorDescription')}")
                return None

    # reCAPTCHA çözme işlemini başlat ve sonucu al
    def solve_recaptcha():
        task_id = create_captcha_task()
        if task_id:
            solution = get_captcha_solution(task_id)
            if solution:
                logging.info(f"reCAPTCHA Çözümü: {solution}")
                return solution
            else:
                logging.error("reCAPTCHA çözümü alınamadı.")
                return None
        else:
            logging.error("Görev oluşturulamadı.")
            return None

    # Tarayıcı işlemleri
    def perform_signup(driver, username, password, email, first_name, last_name):
        try:
            wait = WebDriverWait(driver, 30)

            # "Join us" butonuna tıklama
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(random.uniform(1, 3))
            driver.execute_script("arguments[0].click();", submit_button)
            logging.info("Kayıt butonuna tıklandı.")

            # İlk reCAPTCHA çözme denemesi
            def solve_and_submit():
                g_recaptcha_response = solve_recaptcha()
                if g_recaptcha_response:
                    driver.execute_script(
                        "document.getElementById('g-recaptcha-response').style.display = 'block';"
                    )
                    driver.execute_script(
                        f"document.getElementById('g-recaptcha-response').value='{g_recaptcha_response}';"
                    )
                    logging.info("reCAPTCHA çözümü g-recaptcha-response alanına manuel olarak yerleştirildi.")

                    # reCAPTCHA checkbox'ını tıkla ve userverify isteğini gönder
                    iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
                    driver.switch_to.frame(iframe)
                    checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                    driver.execute_script("arguments[0].click();", checkbox)
                    driver.switch_to.default_content()
                    
                    time.sleep(random.uniform(3, 5))

                    # userverify isteği
                    driver.execute_script(f"""
                        fetch('https://recaptcha.net/recaptcha/api2/userverify?k=6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }},
                            body: 'response={g_recaptcha_response}'
                        }}).then(response => console.log('userverify sonucu:', response));
                    """)

                    # signup isteği
                    driver.execute_script(f"""
                        fetch('/signup', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }},
                            body: 'username={username}&password={password}&email={email}&first_name={first_name}&last_name={last_name}'
                        }}).then(response => console.log('signup sonucu:', response));
                    """)
                    logging.info("signup isteği gönderildi.")
                else:
                    logging.error("reCAPTCHA çözümü alınamadı.")
                    return False
                return True

            # İlk çözüm denemesi
            if not solve_and_submit():
                logging.error("İlk reCAPTCHA çözüm başarısız oldu.")

            # Başarı durumunu kontrol et ve ekran görüntüsü al
            time.sleep(random.uniform(3, 5))
            page_source = driver.page_source
            if "Signed up successfully" in page_source:
                logging.info("Kayıt başarılı, ekran görüntüsü alınıyor.")
                driver.save_screenshot("/vagrant/success_screenshot.png")
            else:
                logging.error("Üyelik başarısız oldu, tekrar çözüm deneniyor.")
                
                # İkinci çözüm denemesi
                if not solve_and_submit():
                    logging.error("İkinci reCAPTCHA çözüm başarısız oldu, kayıt başarısız.")
                else:
                    page_source = driver.page_source
                    if "Signed up successfully" in page_source:
                        logging.info("Kayıt başarılı, ekran görüntüsü alınıyor.")
                        driver.save_screenshot("/vagrant/success_screenshot.png")
                    else:
                        logging.error("Üyelik yine başarısız oldu, farklı bir çözüm arayın.")
                        driver.save_screenshot("/vagrant/error_screenshot.png")

        except Exception as e:
            logging.error(f"Kayıt işlemi sırasında hata oluştu: {e}")
            driver.save_screenshot("/vagrant/error_screenshot_full.png")
        finally:
            time.sleep(500)
            driver.quit()