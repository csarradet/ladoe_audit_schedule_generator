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
    slices = [(57, 63, 63, 65, 65, 66),
              (66, 72, 72, 74, 74, 75),
              (75, 81, 81, 83, 83, 84),
              (84, 90, 90, 92, 92, 93),
              (93, 99, 99, 101, 101, 102)]
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

    def to_str(self):
        return f'100s: {str(self.store_100)}' + '\n' + f'200s: {str(self.store_200s)}'

    def add_100(self, row):
        # 1:1 mapping for 100 records, keep only the most recent
        key = row[19:28]  # SSN
        self.store_100[key] = row

    def add_100s(self, rows):
        for i in rows:
            self.add_100(i)

    def add_200(self, row):
        # 1:many for 200 records, storing them as a list keyed by SSN
        key = row[19:28]  # SSN
        self.store_200s[key].append(row)

    def add_200s(self, rows):
        for i in rows:
            self.add_200(i)

    def get_100(self, key):
        return self.store_100[key]

    def get_200(self, key):
        # Returns the FIRST inserted 200 record, others may exist
        return self.store_200s[key][0]

    def get_200s(self, key):
        # Returns all 200 records inserted for that SSN
        return self.store_200s[key]

    def get_all_keys(self):
        # Returns all IDs passed in from 100 records
        return list(self.store_100)

    def get_name(self, key):
        return self.get_100(key)[28:81]

    def get_years_xp(self, key):
        return self.get_100(key)[97:99]

    def get_cert_num(self, key):
        return self.get_100(key)[87:93]

    def get_cert_type(self, key):
        return self.get_100(key)[83:87]

    def get_ed_level(self, key):
        return self.get_100(key)[95:97]

    def get_days_employed(self, key):
        return self.get_100(key)[118:123]

    def get_emp_type(self, key):
        return self.get_100(key)[117:118]

    def get_pip_salary(self, key):
        return int(self.get_100(key)[103:109])

    def get_retiree_code(self, key):
        return self.get_100(key)[99:101]

    def get_cert_exc_code(self, key):
        return self.get_100(key)[94:95]

    def get_obj_code(self, key):
        return self.get_200(key)[36:39]

    def get_func_code(self, key):
        return self.get_200(key)[39:43]

    def get_total_salary_amount(self, key):
        return int(self.get_100(key)[109:115])

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

    def validate_salary(self, key):
        total_sal = self.get_total_salary_amount(key)
        pip_sal = self.get_pip_salary(key)
        extra_sal = self.get_extra_compensation(key)
        base_sal = self.get_base_salary(key)
        sum_total_sal = pip_sal + extra_sal + base_sal

        if total_sal != sum_total_sal:
            raise ValueError(f'Inconsistent PEP records for {key} - total salary {total_sal} does not equal sum of PEP200 salary records {sum_total_sal}')
