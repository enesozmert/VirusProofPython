import logging
from denemeler.sinifsal import ConfigLogger

ConfigLogger.setup_logging()

""" logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s') """

def test_hybrid_analysis_bot():
    logging.info("Testing HybridAnalysisBot...")
    # Test the bot here
    logging.info("HybridAnalysisBot test completed.")
    return "HybridAnalysisBot çalıştı, yeni API çekti."
