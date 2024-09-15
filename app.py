from flask import Flask, render_template
import signal
import sys
from flask_cors import CORS
import logging
from update_data import fetch_and_update_data
from visualize import create_plot
from database import execute_query, fetch_data
from queryforchart import run_query_for_chart

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
CORS(app)

def signal_handler(sig, frame):
    logging.info('Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.route('/plot')
def index():
    logging.info('Rendering index page')
    try:
        query = "SELECT * FROM your_table"
        data = fetch_data(query)
        logging.info(f"Database connection successful, fetched data: {data}")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
    create_plot()
    return render_template('plot.html')

if __name__ == '__main__':
    logging.info('Starting fetch_and_update_data')
    fetch_and_update_data.start()
    logging.info('Running query for chart')
    run_query_for_chart()
    logging.info('Starting Flask app')
    app.run(host="0.0.0.0", debug=True, port=7777)
