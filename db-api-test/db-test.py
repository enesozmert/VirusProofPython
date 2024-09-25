import pymssql

# Veritabanı bağlantı bilgileri
server = '94.154.34.227'
database = 'VirusProofs'
username = 'vpdbsecurepython'
password = 'vpdbSecurePython@2024!Password#7$'

try:
    # Veritabanına bağlanmayı deniyoruz
    connection = pymssql.connect(server=server, user=username, password=password, database=database)
    print("Veritabanı bağlantısı başarılı!")
    connection.close()

except pymssql.Error as e:
    print(f"Veritabanı bağlantısında hata oluştu: {e}")
