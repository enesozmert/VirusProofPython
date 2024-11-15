import logging

class ConfigLogger:
    @staticmethod
    def setup_logging():
        # Ana logging ayarları
        logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')

        # Selenium ve WebDriver loglarını filtreleme
        #logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
        #logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

