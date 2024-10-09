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
    score = 100  # Start with 100 points
    log_unranked = []
    
    for av_name, details in scan_data.items():
        category = details['category'].lower()
        
        # Skip "clean" or "file type unsupported"
        if category in ['clean', 'file type unsupported']:
            logging.info(f"Skipping {av_name} - Category: {category}")
            continue
        
        # Find the antivirus rank
        rank_info = None
        for rank in av_ranks:
            if rank['name'].lower() == av_name.lower():
                rank_info = rank
                break
        
        if not rank_info:
            log_unranked.append(av_name)
            logging.warning(f"AV rank not found for {av_name}")
            continue
        
        # Apply a penalty based on rank
        penalty = rank_info.get('score', 0)  # Assuming score is stored
        logging.info(f"Applying penalty for {av_name}: {penalty}")
        score -= penalty  # Deduct penalty from score
    
    # Ensure the score doesn't go below 0
    score = max(score, 0)
    
    # Log the final score
    logging.info(f"Final Score after calculation: {score}")
    
    return {"score": score, "details": log_unranked}  # Score ve logları döndür

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
    
    # final_result içindeki score'u tam sayıya çevirelim
    final_score = final_result.get("score", 0)
    
    return {"message": "Algorithm executed successfully", "data": final_score}

# Eğer bu dosya direkt çalıştırılırsa
if __name__ == "__main__":
    test_scanGuid = "sample-scan-guid"
    result = run_calculate(test_scanGuid)
    logging.info(f"Test result: {result}")
    print(result)

