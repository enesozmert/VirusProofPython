import logging

class ConfigLogger:
    @staticmethod
    def setup_logging():
        logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
