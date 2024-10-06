import logging
import requests
import json

# Log settings
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# JSON dosyasının yolu
JSON_FILE = 'avcomperative.json'

def fetch_scan_data(scanGuid):
    """scanGuid kullanarak API'den tarama verilerini getirir."""
    logging.info(f"Fetching scan data for scanGuid: {scanGuid}")
    api_url = f"http://localhost:5000/api/ScanDataResults/getfieldmappingresultdata?scanGuid={scanGuid}"
    try:
        # POST yerine GET metodu ile istek yap
        response = requests.get(api_url)
        response.raise_for_status()  # Hata varsa fırlat
        data = response.json()
        
        # Gelen veriyi JSON stringinden objeye çevir
        scan_data_str = data["data"][0]  # API'den gelen ilk kayıt
        scan_data = json.loads(scan_data_str)
        
        logging.info("Scan data fetched and parsed successfully.")
        return scan_data["data"]  # 'data' alanını döndür
    except requests.RequestException as e:
        logging.error(f"Error fetching scan data: {e}")
        return None

def load_av_comparative_data():
    """avcomperative.json dosyasını yükler."""
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading AV Comparative data: {e}")
        return []

def calculate_score(scan_data, av_ranks):
    total_score = 0
    total_engines = 0
    log_unranked = []  # Rank olmayanları log için tutacağız
    
    for av_name, av_result in scan_data.items():
        av_status = av_result.get("category", "")

        if av_status and av_status.lower() in ["clean", "file type unsupported"]:
            score = 1  # Clean'ler + puan
        else:
            score = -1  # Diğerleri - puan
        
        # 'name' alanını kullanarak antivirüs adı ile eşleştirme yapıyoruz
        rank_info = None
        for rank in av_ranks:
            if rank['name'].lower() == av_name.lower():  # Antivirüs adını kontrol et
                rank_info = rank
                break
        
        if not rank_info:
            log_unranked.append(av_name)
            continue  # Rank'ı olmayan antivirüsü geçiyoruz
        
        rank_multiplier = rank_info['score'] / 10  # 10 üzerinden normalize ediyoruz
        total_score += score * rank_multiplier
        total_engines += 1

    # Loglamak için rank'ı olmayan antivirüsler
    if log_unranked:
        logging.info(f"Rank bilgisi olmayan antivirüs motorları: {', '.join(log_unranked)}")
    
    if total_engines == 0:
        return 0  # Eğer antivirüs motoru yoksa sonuç 0
    
    # Final skoru tam sayıya yuvarlayarak döndür
    final_score = round((total_score / total_engines) * 100)
    
    return int(final_score)  # Tam sayı formatında döndür


def run_calculate(scan_guid):
    logging.info(f"Running calculate process for scanGuid: {scan_guid}")
    
    # Scan verilerini çek
    scan_data = fetch_scan_data(scan_guid)
    if scan_data is None:
        return "Error fetching scan data"
    
    # AV Comparative verilerini yükle
    av_ranks = load_av_comparative_data()
    if not av_ranks:
        return "Error loading AV comparative data"
    
    # Puanı hesapla
    final_score = calculate_score(scan_data, av_ranks)
    return f"{final_score}"

# Eğer bu dosya direkt çalıştırılırsa
if __name__ == "__main__":
    test_scanGuid = "sample-scan-guid"
    result = run_calculate(test_scanGuid)
    logging.info(f"Test result: {result}")
    print(result)
