import logging
from .virustotalbot_proxy import get_working_proxy
from .virustotalbot_mail import get_temp_mail
from .virustotalbot_pre import main as prebrowser
import json
from denemeler.sinifsal import ConfigLogger

ConfigLogger.setup_logging()

""" logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s') """

def test_virustotal_bot():
    logging.info("Starting VirusTotalBot...")

    # Proxy alma işlemi
    proxy = get_working_proxy()
    if proxy:
        logging.info(f"Using proxy: {proxy}")
    else:
        logging.error("No working proxy available. Exiting.")
        return
    # VirusTotal'a kayıt
    prebrowser()

if __name__ == "__main__":
    test_virustotal_bot()

    # Python'da if __name__ == "__main__": bloğu, bir Python dosyasının doğrudan çalıştırıldığında belirli bir kodun çalıştırılmasını sağlar.
    # Bu blok içindeki kod, dosya doğrudan çalıştırıldığında çalışır, ancak dosya bir modül olarak içe aktarıldığında çalışmaz.
