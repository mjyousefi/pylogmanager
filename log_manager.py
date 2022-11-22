from singleton_meta import SingletonMeta
from threading import Thread, Lock
from elasticsearch import Elasticsearch
from datetime import datetime, timezone
import pytz
import traceback


class LogManager(metaclass=SingletonMeta):

    _instance = None

    #Elastic Properties
    _es : Elasticsearch
    _index_name : str

    #Config Properties
    _debug_log_is_enabled: bool
    _info_log_is_enabled: bool

    #Thread Properties
    logger_lock = Lock()


    def __init__(self, elastic_host, elastic_default_index_prefix, debug_log_is_enabled = True, info_log_is_enabled= True):
        try:
            #set properties
            self._debug_log_is_enabled = debug_log_is_enabled
            self._info_log_is_enabled = info_log_is_enabled


            print(elastic_host)
            #first init index name based on prefix (in config) and current datetime
            current_year_month = datetime.today().strftime('%Y%m')
            self._index_name = f'{elastic_default_index_prefix}_{current_year_month}'

            #connect to elastic cloud
            self._es = Elasticsearch(f'{elastic_host}', max_retries=3, retry_on_timeout=True)

            #create index if not exists
            index_exists = self._es.indices.exists(index=self._index_name)
            if not index_exists:
                settings = {}
                mappings = {}
                self._es.indices.create(index=self._index_name, settings=settings, mappings=mappings)

            self.log_info('Log Manager Started Successfully', "initialize")
        except Exception as e:
            self._debug_log_is_enabled = False
            self._info_log_is_enabled = False
            self._index_name = ""
            self.es = None

            #=========
            if hasattr(e, 'message'):
                #repr() function returns a printable representation of the given object
                exception_message = repr(e.message0)
            else:
                exception_message = repr(e)
            doc = {"message": exception_message,
                "@timestamp": datetime.utcnow().isoformat(),
                "level": "EXCEPTION",
                "traceback": traceback.format_exc(),
            }
            with open("elastic_info.txt", "w") as txt_file:
                txt_file.write(str(doc))
                txt_file.close()


    def log_info(self, message: str, action_name = 'default') :
        if self._info_log_is_enabled:
            doc = self._create_message_doc(message, action_name, "INFO")
            self._submit_log(doc)


    def log_debug(self, message: str, action_name = 'default') :
        if self._debug_log_is_enabled:
            doc = self._create_message_doc(message, action_name, "DEBUG")
            self._submit_log(doc)


    def log_error(self, message: str, action_name = 'default') :
        doc = self._create_message_doc(message, action_name, "ERROR")
        self._submit_log(doc)


    def log_exception(self, message: str, action_name = 'default') :
        doc = self._create_message_doc(message, action_name, "EXCEPTION")
        self._submit_log(doc)


    def _create_message_doc(self, message, action_name, level):
        doc = {"message": str(message),
            "@timestamp": datetime.now(pytz.timezone('Asia/Tehran')).isoformat(),
            "level": level,
            "actionName": action_name,
            }
        if level == "EXCEPTION":
            doc["traceback"] = traceback.format_exc()
        return doc


    def _submit_log(self, doc):
        t1 = Thread(target=self._worker, args=[doc, self.logger_lock])
        t1.start()

    def _worker(self, doc, lock):
        with lock:
            if self._es == None:
                print(doc)
                return
            index_exists = self._es.indices.exists(index=self._index_name)
            if index_exists:
                self._es.index(index=self._index_name, body=doc)