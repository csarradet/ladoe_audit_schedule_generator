# Provides a convenient interface for storing and querying info from PEP flat text records


class PepRepo(object):
    def __init__(self):
        self.store_100 = {}

    def add_100(self, row):
        # 1:1 mapping for 100 records, keep only the most recent
        key = row[20:29]  # SSN
        self.store_100[key] = row

    def get_100(self, key):
        return self.store_100[key]

    def get_name(self, key):
        return self.get_100(key)[29:82]
