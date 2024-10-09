import logging
from rank import run_rank_update  # Import the rank update function
from calculate import run_calculate  # Import the calculate function


# Log settings
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def main(scan_guid):
    logging.info("Starting the algorithm (rank update)...")
    update_result = run_rank_update()  # Rank güncellemesini çalıştır
    
    logging.info(f"Rank update result: {update_result}")  # Sonucu logla
    
    logging.info(f"Starting the calculate process for scanGuid: {scan_guid}...")
    calculate_result = run_calculate(scan_guid)  # Burada hesaplama yapılıyor
    
    logging.info(f"Calculate result: {calculate_result}")  # Sonucu logla
    
    if isinstance(calculate_result, dict):
        # Eğer calculate_result bir dict ise, doğrudan döndür
        return {
            "message": update_result,
            "data": calculate_result
        }
    else:
        # Eğer int'e dönüştürülebilecek bir şeyse int'e çevir
        return {
            "message": update_result,
            "data": int(calculate_result)
        }

if __name__ == "__main__":
    # Test etmek için bir scan_guid verin
    test_scan_guid = "sample_scan_guid"  # Gerçek bir scanGuid kullanarak test edin
    result = main(test_scan_guid)
    logging.info(f"Final result: {result}")  # Log the final result from both processes
    print(result)
