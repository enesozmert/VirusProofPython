import logging
from calculate import run_calculate  # Import the calculate function

# Log settings
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def main(scan_guid):
    logging.info(f"Starting the calculate process for scanGuid: {scan_guid}...")
    calculate_result = run_calculate(scan_guid)  # Hesaplama fonksiyonu
    
    logging.info(f"Calculate result: {calculate_result}")  # Sonucu logla
    
    # Frontend'in beklediği formatta sonucu döndür
    if isinstance(calculate_result, int):
        return {
            "result": {
                "data": calculate_result,  # Hesaplanan sonuç
            }
        }
    else:
        # Eğer hesaplama sonucu bir dict ise
        return {
            "result": {
                "data": calculate_result.get("data", 0),  # Dict'teki 'data' kısmını al
            }
        }

if __name__ == "__main__":
    # Test için bir scan_guid ver
    test_scan_guid = "sample_scan_guid"
    result = main(test_scan_guid)
    logging.info(f"Final result: {result}")
    print(result)
