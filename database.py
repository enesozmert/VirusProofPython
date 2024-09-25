import pyodbc
import logging
import hashlib

# Loglama ayarları, tüm loglar '/vagrant/pythonapp.log' dosyasına yazılacak
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Veritabanı bağlantı dizesi
conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=94.154.34.227;'
            'DATABASE=VirusProofs;'
            'UID=vpdbsecurepython;'  # Yeni kullanıcı adı
            'PWD=vpdbSecurePython@2024!Password#7$;'  # Şifre doğrudan burada
            'TrustServerCertificate=yes;')

# Veritabanı bağlantısını kuran fonksiyon
def get_connection():
    logging.debug('Establishing database connection')
    return pyodbc.connect(conn_str)

# Veritabanı sorgusu çalıştıran fonksiyon
def execute_query(query, params=None):
    conn = None
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
        if conn is not None:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

# Veritabanından veri çeken fonksiyon
def fetch_data(query, params=None):
    conn = None
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
        if conn is not None:
            if 'cursor' in locals():
                cursor.close()
            conn.close()
