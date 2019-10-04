import unittest
from pep_repo import PepRepo


def str_insert(original_str, new_text, starting_pos):
    return original_str[:starting_pos] + new_text + original_str[starting_pos + len(new_text):]


_SSN = '000000001'
_NAME = 'BOB' + (' ' * 50)
_YEARS_XP = '01'
_CERT_NUM = '123456'
_CERT_TYPE = 'ABCD'
_ED_LEVEL = '11'
_DAYS_EMPLOYED = '12345'
_EMP_TYPE = 'F'
_PIP_SALARY = '100100'
_PIP_SALARY_INT = int(_PIP_SALARY)
_RETIREE_CODE = '01'
_CERT_EXC_CODE = '5'


def dummy_pep_100(ssn=_SSN,
                  name=_NAME,
                  years_xp=_YEARS_XP,
                  cert_num=_CERT_NUM,
                  cert_type=_CERT_TYPE,
                  ed_level=_ED_LEVEL,
                  days_employed=_DAYS_EMPLOYED,
                  emp_type=_EMP_TYPE,
                  pip_salary=_PIP_SALARY,
                  retiree_code=_RETIREE_CODE,
                  cert_exc_code=_CERT_EXC_CODE):
    # Generates a dummy row of PEP 100 data that can be inserted into a PepRepo
    line = " " * 188  # Start with all blanks of appropriate length
    line = str_insert(line, ssn, 20)
    line = str_insert(line, name, 29)
    line = str_insert(line, years_xp, 98)
    line = str_insert(line, cert_num, 88)
    line = str_insert(line, cert_type, 84)
    line = str_insert(line, ed_level, 96)
    line = str_insert(line, days_employed, 119)
    line = str_insert(line, emp_type, 118)
    line = str_insert(line, pip_salary, 104)
    line = str_insert(line, retiree_code, 100)
    line = str_insert(line, cert_exc_code, 95)
    return line


class TestUtils(unittest.TestCase):
    def test_str_insert(self):
        # Only used internally, not testing it exhaustively
        t = 'foobarbaz'
        new_t = str_insert(t, 'NEW', 0)
        self.assertEqual(new_t, 'NEWbarbaz')
        new_t = str_insert(t, 'NEW', 3)
        self.assertEqual(new_t, 'fooNEWbaz')
        new_t = str_insert(t, 'NEW', 6)
        self.assertEqual(new_t, 'foobarNEW')
        new_t = str_insert(t, 'NEW', len(t))
        self.assertEqual(new_t, 'foobarbazNEW')


class TestPepRepo(unittest.TestCase):
    def setUp(self):
        self.repo = PepRepo()
        self.repo.add_100(dummy_pep_100())

    def test_get_100(self):
        self.repo = PepRepo()
        rec = dummy_pep_100()
        self.repo.add_100(rec)
        found = self.repo.get_100(_SSN)
        self.assertEqual(found, rec)

    def test_get_name(self):
        self.assertEqual(_NAME, self.repo.get_name(_SSN))

    def test_get_years_xp(self):
        self.assertEqual(_YEARS_XP, self.repo.get_years_xp(_SSN))

    def test_get_cert_num(self):
        self.assertEqual(_CERT_NUM, self.repo.get_cert_num(_SSN))

    def test_get_cert_type(self):
        self.assertEqual(_CERT_TYPE, self.repo.get_cert_type(_SSN))

    def test_get_ed_level(self):
        self.assertEqual(_ED_LEVEL, self.repo.get_ed_level(_SSN))

    def test_get_days_employed(self):
        self.assertEqual(_DAYS_EMPLOYED, self.repo.get_days_employed(_SSN))

    def test_get_emp_type(self):
        self.assertEqual(_EMP_TYPE, self.repo.get_emp_type(_SSN))

    def test_get_pip_salary(self):
        self.assertEqual(_PIP_SALARY_INT, self.repo.get_pip_salary(_SSN))

    def test_get_retiree_code(self):
        self.assertEqual(_RETIREE_CODE, self.repo.get_retiree_code(_SSN))

    def test_get_cert_exc_code(self):
        self.assertEqual(_CERT_EXC_CODE, self.repo.get_cert_exc_code(_SSN))
