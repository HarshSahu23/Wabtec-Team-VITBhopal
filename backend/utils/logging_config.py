import logging

def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('data_handler.log'),
            logging.StreamHandler()
        ]
    )
