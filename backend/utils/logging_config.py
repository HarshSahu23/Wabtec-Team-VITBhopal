import logging

def configure_logging():
    """Configure logging for the application."""
    log_file = 'data_handler.log'
    handlers = [logging.FileHandler(log_file)]

    # Only add StreamHandler if running with console
    # if sys.stdout is not None:
    #     handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=handlers
    )
