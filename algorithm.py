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
    
    # Eğer calculate_result bir dict ise içinden data alanını çekiyoruz
    if isinstance(calculate_result, dict) and 'data' in calculate_result:
        return {
            "result": {
                "data": calculate_result['data'],  # Burada data kısmını integer olarak alıyoruz
                "message": "Algorithm executed successfully"
            }
        }
    else:
        return {
            "result": {
                "data": int(calculate_result),  # Eğer dict değilse doğrudan integer'a çeviriyoruz
                "message": "Algorithm executed successfully"
            }
        }

if __name__ == "__main__":
    # Test etmek için bir scan_guid verin
    test_scan_guid = "sample_scan_guid"  # Gerçek bir scanGuid kullanarak test edin
    result = main(test_scan_guid)
    logging.info(f"Final result: {result}")  # Log the final result from both processes
    print(result)
