import logging

# Log settings (if calculate.py is run independently)
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def run_calculate():
    logging.info("Starting calculation in calculate.py...")
    print("test")  # This will print to the console
    logging.info("Calculation completed in calculate.py.")
    return "Calculation complete"

if __name__ == "__main__":
    run_calculate()  # Run calculate if this file is executed directly
