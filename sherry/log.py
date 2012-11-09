import logging

class RollingMemoryHandler(logging.Handler):

    def __init__(self, max_records=50, *args, **kwargs):
        self.records = []
        self.max_records = max_records
        super(RollingMemoryHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        self.records.append(record)
        if len(self.records) > self.max_records:
            del self.records[0]
