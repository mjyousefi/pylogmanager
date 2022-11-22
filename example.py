#Utils File
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
    
    
#Craete Log    
from log_manager_utils import LogManagerUtils

app_log_manager = LogManagerUtils.get_log_manager()


#log debug
app_log_manager.log_debug('ExampleLog', action_name='TestLog')


#log exception
try:
    content = a / 2
except Exception as e:
    if hasattr(e, 'message'):
        exception_message = repr(e.message0)
    else:
        exception_message = repr(e)
    message={"Exception":exception_message}
    app_log_manager.log_exception(message, action_name='APICalled')
