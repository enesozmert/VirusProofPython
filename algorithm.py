import logging
from rank import run_rank_update  # Import the rank update function
from calculate import run_calculate  # Import the calculate function

# Log settings
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def main():
    logging.info("Starting the algorithm (rank update)...")
    
    # Run the rank update first
    update_result = run_rank_update()
    logging.info(update_result)  # Log the result from rank.py
    
    # Run the calculate process
    logging.info("Starting the calculate process...")
    calculate_result = run_calculate()  # Assuming this function is in calculate.py
    logging.info(calculate_result)
    
    return update_result, calculate_result

if __name__ == "__main__":
    result = main()
    logging.info(f"Final result: {result}")  # Log the final result from both processes
