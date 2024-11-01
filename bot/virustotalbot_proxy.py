import logging
import requests
from denemeler.sinifsal import ConfigLogger
from concurrent.futures import ThreadPoolExecutor, as_completed

ConfigLogger.setup_logging()

""" logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s') """

# Proxy sağlayıcısından dinamik liste alalım
# Proxy listesini çek
def fetch_proxies():
    logging.info("Fetching proxies from the provider...")
    try:
        response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies.json")
        response.raise_for_status()
        proxies_data = response.json()
        proxies = [f"http://{proxy['host']}:{proxy['port']}" for proxy in proxies_data if proxy['protocol'] == 'http']
        logging.info(f"Fetched {len(proxies)} HTTP proxies.")
        return proxies
    except requests.RequestException as e:
        logging.error(f"Failed to fetch proxies: {e}")
        return []

# Proxy'nin çalışıp çalışmadığını test et
def test_proxy(proxy):
    try:
        response = requests.get("http://ipinfo.io", proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

# İlk çalışan proxy'yi bul
def get_working_proxy():
    proxy_list = fetch_proxies()
    if not proxy_list:
        logging.error("No proxies available.")
        return None

    logging.info("Testing proxies in batches of 10.")
    # 10'lu gruplar halinde proxy denemesi yapalım
    for i in range(0, len(proxy_list), 10):
        batch = proxy_list[i:i + 10]
        logging.info(f"Testing batch: {batch}")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in batch}
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():  # Eğer proxy başarılıysa
                        logging.info(f"Working proxy found: {proxy}")
                        return proxy
                    else:
                        logging.warning(f"Proxy failed: {proxy}")
                except Exception as e:
                    logging.warning(f"Error testing proxy {proxy}: {e}")

    logging.error("No working proxy found in any batch.")
    return None

# Proxy'nin çalışıp çalışmadığını kontrol eden fonksiyon
def test_proxy(proxy):
    try:
        response = requests.get("http://ipinfo.io", proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            logging.info(f"Proxy worked! {response.json()}")
            return True
        else:
            logging.error(f"Proxy failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Proxy failed: {e}")
        return False
