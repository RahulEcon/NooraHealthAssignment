import logging

def log(module:str=__name__):
    # Figure out which module returned the log message
    logger=logging.getLogger(module)
    logger.setLevel(logging.INFO)
    # Location of the logger
    handler=logging.FileHandler('update.log')
    # Format of the log message
    format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %I:%M:%S %p')
    handler.setFormatter(format)
    logger.addHandler(handler)
    return logger