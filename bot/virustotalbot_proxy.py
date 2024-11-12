import logging
import requests
from denemeler.sinifsal import ConfigLogger
from concurrent.futures import ThreadPoolExecutor, as_completed

ConfigLogger.setup_logging()

# Başarısız proxyleri hafızada tut
failed_proxies = set()

# Proxy sağlayıcısından dinamik liste alalım
def fetch_proxies():
    logging.info("Fetching proxies from the provider...")
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies.json"
        )
        response.raise_for_status()
        proxies_data = response.json()
        proxies = [
            f"http://{proxy['host']}:{proxy['port']}"
            for proxy in proxies_data
            if proxy["protocol"] == "http"
        ]
        logging.info(f"Fetched {len(proxies)} HTTP proxies.")
        return proxies
    except requests.RequestException as e:
        logging.error(f"Failed to fetch proxies: {e}")
        return []

# Proxy'nin çalışıp çalışmadığını test eden fonksiyon
def test_proxy(proxy):
    if proxy in failed_proxies:
        logging.info(f"Skipping previously failed proxy: {proxy}")
        return False

    try:
        # Google reCAPTCHA API'ye erişimi kontrol et
        recaptcha_response = requests.get(
            "https://www.google.com/recaptcha/api/siteverify",
            proxies={"http": proxy, "https": proxy},
            timeout=10,
        )
        if recaptcha_response.status_code != 200:
            failed_proxies.add(proxy)
            logging.info(f"Proxy failed on Google reCAPTCHA check: {proxy}")
            return False

        # VirusTotal'e erişimi kontrol et
        virustotal_response = requests.get(
            "https://www.virustotal.com",
            proxies={"http": proxy, "https": proxy},
            timeout=10,
        )
        if virustotal_response.status_code == 200:
            logging.info(f"Working proxy found: {proxy}")
            return True
        else:
            failed_proxies.add(proxy)
            logging.info(f"Proxy failed on VirusTotal: {proxy}")
            return False
    except requests.RequestException:
        failed_proxies.add(proxy)
        logging.info(f"RequestException for proxy: {proxy}")
        return False

# Çalışan ilk proxy'yi bul
def get_working_proxy():
    proxy_list = fetch_proxies()
    if not proxy_list:
        logging.error("No proxies available.")
        return None

    logging.info("Testing proxies in batches of 50.")
    for i in range(0, len(proxy_list), 50):
        batch = [proxy for proxy in proxy_list[i:i + 50] if proxy not in failed_proxies]
        logging.info(f"Testing batch of {len(batch)} proxies.")

        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_proxy = {
                executor.submit(test_proxy, proxy): proxy for proxy in batch
            }

            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():  # Eğer proxy başarılıysa
                        logging.info(f"Working proxy selected: {proxy}")
                        return proxy
                except Exception as e:
                    logging.warning(f"Error testing proxy {proxy}: {e}")

    logging.error("No working proxy found in any batch.")
    return None

if __name__ == "__main__":
    selected_proxy = get_working_proxy()
    if selected_proxy:
        logging.info(f"Selected proxy for usage: {selected_proxy}")
    else:
        logging.error("No proxy could be selected.")
