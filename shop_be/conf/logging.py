import json
from copy import deepcopy
from typing import Dict

import ujson
from pythonjsonlogger import jsonlogger

from shop_be.conf.settings import settings, Env


class BaseJsonFormatter(jsonlogger.JsonFormatter):
    FILTERED_SECURE_DATA = ['card_cvv', 'card_month', 'card_year', 'token']

    def _filter_json(self, json_log: Dict) -> Dict:
        if json_log and isinstance(json_log, dict):
            for key, value in json_log.copy().items():
                if key in self.FILTERED_SECURE_DATA:
                    json_log[key] = '***'

                if isinstance(value, dict):
                    json_log[key] = self._filter_json(value)
        return json_log

    def _filter_text(self, json_log: str) -> str:
        if isinstance(json_log, str):
            try:
                log = ujson.loads(json_log or '{}')
            except ujson.JSONDecodeError:
                log = json_log
        else:
            log = json_log

        filtered_log = self._filter_json(log)
        return json.dumps(log or filtered_log)

    def add_fields(self, log_record, record, message_dict):
        super(BaseJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        if isinstance(record.msg, dict):
            log_record['json'] = self._filter_json(deepcopy(record.msg.get('json')))
            log_record['text'] = self._filter_text(deepcopy(record.msg.get('text')))


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': BaseJsonFormatter,
        },
        'uvicorn_json': {
            '()': BaseJsonFormatter,
        },
        'local': {
            '()': 'logging.Formatter',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'gunicorn_uvicorn': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'uvicorn_json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'uvicorn': {'handlers': [], 'level': settings.LOG_LEVEL},
        'gunicorn': {'handlers': ['gunicorn_uvicorn'], 'level': settings.LOG_LEVEL},
        'gunicorn.access': {'handlers': ['gunicorn_uvicorn'], 'level': settings.LOG_LEVEL},
        'gunicorn.error': {'handlers': ['gunicorn_uvicorn'], 'level': settings.LOG_LEVEL},
    },
    'root': {'handlers': ['default'], 'level': settings.LOG_LEVEL}
}
