import logging
import logging.config
import os


# Create the Logger
loggers = logging.getLogger(__name__)
loggers.setLevel(logging.DEBUG)

# Create path for logger
path = os.path.join(os.path.dirname(__file__), 'log.txt')
# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(filename=path)
logger_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
loggers.addHandler(logger_handler)
loggers.info('Completed configuring logger()!')
