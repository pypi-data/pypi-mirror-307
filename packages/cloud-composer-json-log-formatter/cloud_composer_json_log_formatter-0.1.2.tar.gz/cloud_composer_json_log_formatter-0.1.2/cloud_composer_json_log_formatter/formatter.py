# json_log_formatter/formatter.py

import json
import logging

class JSONFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%", json_fields=None):
        super().__init__(fmt, datefmt, style)
        if json_fields is None:
            json_fields = []
        self.json_fields = json_fields

    def usesTime(self):
        return "asctime" in self.json_fields

    def format(self, record):
        super().format(record)
        record_dict = {label: getattr(record, label, None) for label in self.json_fields}
        if "message" in self.json_fields:
            msg = record_dict["message"]
            if record.exc_text:
                if msg[-1:] != "\n":
                    msg = msg + "\n"
                msg = msg + record.exc_text
            if record.stack_info:
                if msg[-1:] != "\n":
                    msg = msg + "\n"
                msg = msg + self.formatStack(record.stack_info)
            record_dict["message"] = msg
        return json.dumps(record_dict)

class ComposerFormatter(JSONFormatter):
    def __init__(self, fmt=None, datefmt=None, style="%", **kwargs):
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            json_fields=['message', 'asctime', 'filename', 'lineno', 'levelname']
        )
