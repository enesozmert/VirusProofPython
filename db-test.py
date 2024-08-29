import pymssql

# Veritabanı bağlantı bilgileri
server = '94.154.34.227'
database = 'VirusProofs'
username = 'vpdbsecure'
password = "lqT1*XTC#@p=1Ke.PaOZ1_m_%ynd&;[yEGe+8o6?)yh9&"

try:
    # Veritabanına bağlanmayı deniyoruz
    connection = pymssql.connect(server, username, password, database)
    print("Veritabanı bağlantısı başarılı!")
    connection.close()

except pymssql.Error as e:
    print(f"Veritabanı bağlantısında hata oluştu: {e}")
