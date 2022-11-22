from log_manager import LogManager
from dotenv import load_dotenv
import os

load_dotenv()

class LogManagerUtils():

    @staticmethod
    def get_log_manager():
        # read config
        elastic_host = os.getenv('ELASTIC_HOST')
        elastic_default_index_prefix = os.getenv('ELASTIC_DEFAULT_INDEX_PREFIX')
        debug_log_is_enabled = os.getenv('ELASTIC_LOG_DEBUG_ENABLED')
        info_log_is_enabled = os.getenv('ELASTIC_LOG_INFO_ENABLED')
        return LogManager(elastic_host, elastic_default_index_prefix, debug_log_is_enabled, info_log_is_enabled)
