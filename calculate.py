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
        response = requests.get(api_url)
        response.raise_for_status()  # Hata varsa fırlat
        data = response.json()
        
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
    initial_score = 100  # Başlangıç puanı
    total_rank_score = 0  # AV rank toplamı
    log_unranked = []  # Rank bulunamayan AV'ler
    av_rank_dict = {}  # AV ranklarını saklayan dict

    # Önce tüm AV ranklarının toplamını 100 puana oranla normalize edelim
    for rank in av_ranks:
        av_name = rank['name'].lower()
        score = rank.get('score', 0)
        total_rank_score += score
        av_rank_dict[av_name] = score  # AV isimlerine göre rankları sakla

    logging.info(f"Total AV rank score before normalization: {total_rank_score}")

    # Rank toplamı 100'e oranlanarak normalize ediliyor
    if total_rank_score > 0:
        normalization_factor = 100 / total_rank_score
    else:
        normalization_factor = 1  # Eğer toplam 0 ise, normalization yapılmaz

    logging.info(f"Normalization factor: {normalization_factor}")

    # Skor hesaplama
    score = initial_score
    for av_name, details in scan_data.items():
        category = details['category'].lower()

        # Clean ve file type unsupported olanları atla
        if category in ['clean', 'file type unsupported']:
            logging.info(f"Skipping {av_name} - Category: {category}")
            continue

        # Antivirüs rank'ini bul
        rank_score = av_rank_dict.get(av_name.lower(), None)
        if rank_score is None:
            log_unranked.append(av_name)
            logging.warning(f"AV rank not found for {av_name}")
            continue

        # Normalize edilmiş rank skorunu kullanarak penaltı uygula
        normalized_penalty = rank_score * normalization_factor
        logging.info(f"Applying penalty for {av_name}: {normalized_penalty}")
        score -= normalized_penalty

    # Skorun 0'ın altına inmesini veya 100'ü geçmesini engelle
    score = max(min(score, 100), 0)

    # Log the final score and unranked AVs
    logging.info(f"Final Score after calculation: {score}")
    logging.info(f"Unranked AVs: {log_unranked}")

    return {"score": round(score), "details": log_unranked}  # Score'u yuvarlayarak döndür

def ispat():
    """avcomperative.json'daki score'ların toplamının 100 puana normalize edilmesini ispat eder."""
    # AV Comparative verilerini yükle
    av_ranks = load_av_comparative_data()

    if not av_ranks:
        logging.error("Error: AV Comparative data could not be loaded for ispat function.")
        return

    # Rank toplamı hesaplama
    total_rank_score = 0
    av_rank_dict = {}

    for rank in av_ranks:
        av_name = rank['name'].lower()
        score = rank.get('score', 0)
        total_rank_score += score
        av_rank_dict[av_name] = score  # AV isimlerine göre rankları sakla

    logging.info(f"Total AV rank score before normalization: {total_rank_score}")

    # Normalization factor hesaplama
    if total_rank_score > 0:
        normalization_factor = 100 / total_rank_score
    else:
        normalization_factor = 1  # Eğer toplam 0 ise normalization yapılmaz

    logging.info(f"Normalization factor: {normalization_factor}")

    # Rank'ları normalize edip toplamın yine 100'e eşit olduğunu kontrol etme
    normalized_total_score = 0
    for av_name, score in av_rank_dict.items():
        normalized_score = score * normalization_factor
        normalized_total_score += normalized_score
        logging.info(f"{av_name.capitalize()} AV's normalized score: {normalized_score}")

    # Loglarda sonuç
    logging.info(f"Final normalized total score: {normalized_total_score}")

    # Sonucu döndürelim
    return normalized_total_score

def run_calculate(scan_guid):
    logging.info(f"Running calculate process for scanGuid: {scan_guid}")
    
    # Scan verilerini çek
    scan_data = fetch_scan_data(scan_guid)
    if scan_data is None:
        return {"message": "Error fetching scan data", "data": None}
    
    # AV Comparative verilerini yükle
    av_ranks = load_av_comparative_data()
    if not av_ranks:
        return {"message": "Error loading AV comparative data", "data": None}
    
    # Puanı hesapla
    final_result = calculate_score(scan_data, av_ranks)
    ispat()

    # final_result içindeki score'u tam sayıya çevirelim
    final_score = final_result.get("score", 0)
    
    return {"message": "Algorithm executed successfully", "data": final_score}

# Eğer bu dosya direkt çalıştırılırsa
if __name__ == "__main__":  # AV rank toplamını ispatla ve loglara yazdır
    test_scanGuid = "sample-scan-guid"
    result = run_calculate(test_scanGuid)
    logging.info(f"Test result: {result}")
    print(result)

