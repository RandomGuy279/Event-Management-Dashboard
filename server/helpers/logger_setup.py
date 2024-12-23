import logging
import logging.config
import json
from .config import configData

LOGGING_CONFIG = None


class Logger:
    def __init__(self, log_config: dict):
        self._configure_logger(log_config)

    def _configure_logger(self, log_config: dict):
        if isinstance(log_config, str):
            log_config = json.loads(log_config)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger
    
logger = Logger(configData["logConfiguration"]).get_logger()