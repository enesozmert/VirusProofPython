import random
import logging
import requests

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Proxy sağlayıcısından dinamik liste alalım
def fetch_proxies():
    logging.info("Fetching proxies from the new provider...")
    try:
        # JSON formatındaki proxy listesini çekiyoruz
        response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies.json")
        response.raise_for_status()
        proxies_data = response.json()
        
        # Sadece 'http' ve 'https' proxy'lerini seçelim
        proxies = [f"http://{proxy['host']}:{proxy['port']}" for proxy in proxies_data if proxy['protocol'] == 'http']
        logging.info(f"Fetched {len(proxies)} HTTP proxies.")
        return proxies
    except requests.RequestException as e:
        logging.error(f"Failed to fetch proxies: {e}")
        return []

# Dinamik proxy listesinden sırasıyla bir proxy seçip deneyelim
def get_working_proxy():
    proxy_list = fetch_proxies()
    if not proxy_list:
        logging.error("No proxies available.")
        return None

    for proxy in proxy_list:
        logging.info(f"Testing proxy: {proxy}")
        if test_proxy(proxy):
            logging.info(f"Proxy succeeded: {proxy}")
            return proxy
        else:
            logging.warning(f"Proxy failed: {proxy}")
    logging.error("No working proxy found.")
    return None

# Proxy'nin çalışıp çalışmadığını kontrol eden fonksiyon
def test_proxy(proxy):
    try:
        # Proxy'nin çalışıp çalışmadığını test etmek için bir istek gönderiyoruz
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

# Main fonksiyonu
def main():
    logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Starting Proxy Test")
    working_proxy = get_working_proxy()
    if working_proxy:
        logging.info(f"Working proxy found: {working_proxy}")
    else:
        logging.error("No working proxy found in the list.")

if __name__ == "__main__":
    main()
