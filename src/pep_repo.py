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

    def get_years_xp(self, key):
        return self.get_100(key)[98:100]

    def get_cert_num(self, key):
        return self.get_100(key)[88:94]

    def get_cert_type(self, key):
        return self.get_100(key)[84:88]

    def get_ed_level(self, key):
        return self.get_100(key)[96:98]

    def get_days_employed(self, key):
        return self.get_100(key)[119:124]

    def get_emp_type(self, key):
        return self.get_100(key)[118:119]

    def get_pip_salary(self, key):
        return int(self.get_100(key)[104:110])

    def get_retiree_code(self, key):
        return self.get_100(key)[100:102]

    def get_cert_exc_code(self, key):
        return self.get_100(key)[95:96]
