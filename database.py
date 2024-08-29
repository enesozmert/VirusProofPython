import pyodbc
import logging

conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=94.154.34.227;'
            'DATABASE=VirusProofs;'
            'UID=vpdbsecure;'
            'PWD=\"lqT1*XTC#@p=1Ke.PaOZ1_m_%ynd&;[yEGe+8o6?)yh9&\";'
            'TrustServerCertificate=yes;')

def get_connection():
    logging.debug('Establishing database connection')
    return pyodbc.connect(conn_str)

def execute_query(query, params=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        logging.info(f'Executed query: {query}')
    except Exception as e:
        logging.error(f'Error executing query: {e}')
    finally:
        cursor.close()
        conn.close()

def fetch_data(query, params=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        logging.info(f'Fetched data with query: {query}')
        return data
    except Exception as e:
        logging.error(f'Error fetching data: {e}')
    finally:
        cursor.close()
        conn.close()
