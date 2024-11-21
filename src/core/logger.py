import logging
import json
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'service': 'library',
            'level': record.levelname,
            'message': record.getMessage(),
            'timestamp': self.formatTime(record, self.datefmt),
            'pathname': record.pathname,
            'lineno': record.lineno,
            'filename': record.filename,
            'func_name': record.funcName,
            'request_id': getattr(record, 'request_id', None)
        }
        return json.dumps(log_record)


def setup_logging(logger_name='library'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger