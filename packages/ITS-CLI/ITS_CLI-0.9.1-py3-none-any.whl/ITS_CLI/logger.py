import logging
import logging.handlers as handlers
import os

LOG_DIR = './log'
LOG_FILENAME = 'smartcs_client.log'
LOG_PATH = LOG_DIR + '/' + LOG_FILENAME

class CustomFormatter(logging.Formatter):
    """Logging Formatter"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_debug = "%(asctime)s:DBG %(module)s: %(message)s"
    format_info  = "%(asctime)s:INF %(module)s: %(message)s"
    format_warn  = "%(asctime)s:WRN %(module)s: %(message)s (%(filename)s:%(lineno)d)"
    format_err   = "%(asctime)s:ERR %(module)s: %(message)s (%(filename)s:%(lineno)d)"
    format_cri   = "%(asctime)s:CRI %(module)s: %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format_debug ,
        logging.INFO: format_info,
        logging.WARNING: format_warn,
        logging.ERROR: format_err,
        logging.CRITICAL: format_cri
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class CustomFileFormatter(logging.Formatter):
    """Logging Formatter"""

    format_debug = "%(asctime)s:DBG %(module)s: %(message)s"
    format_info  = "%(asctime)s:INF %(module)s: %(message)s"
    format_warn  = "%(asctime)s:WRN %(module)s: %(message)s (%(filename)s:%(lineno)d)"
    format_err   = "%(asctime)s:ERR %(module)s: %(message)s (%(filename)s:%(lineno)d)"
    format_cri   = "%(asctime)s:CRI %(module)s: %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format_debug,
        logging.INFO: format_info,
        logging.WARNING: format_warn,
        logging.ERROR: format_err,
        logging.CRITICAL: format_cri
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# level: DEBUG, INFO, WARNING, ERROR, CRITICAL
Logger = logging.getLogger(__name__)
Logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())
Logger.addHandler(console_handler)

file_handler = handlers.RotatingFileHandler(filename=LOG_PATH, maxBytes=10000000, backupCount=24)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())
Logger.addHandler(file_handler)
