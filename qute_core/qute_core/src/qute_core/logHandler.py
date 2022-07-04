import logging
import logging.config
from os import path


class LogHandler(object):

    def __init__(self):
        log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
        logging.config.fileConfig(log_file_path)
        self.logging = logging.getLogger()

    def log(self):
        return self.logging
