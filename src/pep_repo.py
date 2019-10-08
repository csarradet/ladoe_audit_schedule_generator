# Provides a convenient interface for storing and querying info from PEP flat text records
from collections import defaultdict


class SalaryOcc(object):
    # Represents one non-zero salary occurrence sourced from a 200 file
    def __init__(self, amount, fund, stype):
        self.amount = amount  # int
        self.fund = fund  # str
        self.stype = stype  # str


def generate_salary_occs(pep200_rec):
    output = []
    # Start:end string slicing args to extract amt/fund/type from a 200 rec,
    # one for each of the five possible locations
    slices = [(58, 64, 64, 66, 66, 67),
              (67, 73, 73, 75, 75, 76),
              (76, 82, 82, 84, 84, 85),
              (85, 91, 91, 93, 93, 94),
              (94, 100, 100, 102, 102, 103)]
    for i in slices:
        amount = int(pep200_rec[i[0]:i[1]])
        fund = pep200_rec[i[2]:i[3]]
        stype = pep200_rec[i[4]:i[5]]
        if amount: output.append(SalaryOcc(amount, fund, stype))
    return output


class PepRepo(object):
    def __init__(self):
        self.store_100 = {}
        self.store_200s = defaultdict(list)

    def add_100(self, row):
        # 1:1 mapping for 100 records, keep only the most recent
        key = row[20:29]  # SSN
        self.store_100[key] = row

    def add_200(self, row):
        # 1:many for 200 records, storing them as a list keyed by SSN
        key = row[20:29]  # SSN
        self.store_200s[key].append(row)

    def get_100(self, key):
        return self.store_100[key]

    def get_200(self, key):
        # Returns the FIRST inserted 200 record, others may exist
        return self.store_200s[key][0]

    def get_200s(self, key):
        # Returns all 200 records inserted for that SSN
        return self.store_200s[key]

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

    def get_obj_code(self, key):
        return self.get_200(key)[37:40]

    def get_func_code(self, key):
        return self.get_200(key)[40:44]

    def get_total_salary_amount(self, key):
        return int(self.get_100(key)[110:116])

    def _get_all_occs(self, key):
        occs = []
        for i in self.get_200s(key):
            occs += generate_salary_occs(i)
        return occs

    def get_extra_compensation(self, key):
        extra_occs = [x for x in self._get_all_occs(key) if x.stype != '1']
        return sum(x.amount for x in extra_occs)

    def get_base_salary(self, key):
        base_occs = [x for x in self._get_all_occs(key) if x.stype == '1']
        return sum(x.amount for x in base_occs)
