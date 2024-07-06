from flask import Flask, render_template
import signal
import sys
from flask_cors import CORS
import logging
from update_data import fetch_and_update_data
from visualize import create_plot
# from isactive import is_active_checker

# Loglama ayarları
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
CORS(app)

# Sinyal işleyiciyi ayarla
def signal_handler(sig, frame):
    logging.info('Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.route('/plot')
def index():
    logging.info('Rendering index page')
    create_plot()
    return render_template('plot.html')

if __name__ == '__main__':
    logging.info('Starting fetch_and_update_data')
    fetch_and_update_data.start()
    logging.info('Starting Flask app')
    app.run(debug=True, port=7777)
