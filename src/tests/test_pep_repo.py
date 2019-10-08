import unittest
from pep_repo import (PepRepo,
                      SalaryOcc,
                      generate_salary_occs)


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
_TOTAL_SALARY_AMT = _PIP_SALARY
_TOTAL_SALARY_AMT_INT = _PIP_SALARY_INT


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
                  cert_exc_code=_CERT_EXC_CODE,
                  total_salary_amt=_TOTAL_SALARY_AMT):
    # Generates a dummy row of PEP data that can be inserted into a PepRepo
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
    line = str_insert(line, total_salary_amt, 110)
    return line


_OBJ_CODE = '123'
_FUNC_CODE = '1234'
_AMT = '0' * 6
_AMT_INT = 0
_FUND = '11'
_STYPE = '2'


def dummy_pep_200(ssn=_SSN,
                  obj_code=_OBJ_CODE,
                  func_code=_FUNC_CODE,
                  amt_1=_AMT,
                  fund_1=_FUND,
                  type_1=_STYPE,

                  amt_2=_AMT,
                  fund_2=_FUND,
                  type_2=_STYPE,

                  amt_3=_AMT,
                  fund_3=_FUND,
                  type_3=_STYPE,

                  amt_4=_AMT,
                  fund_4=_FUND,
                  type_4=_STYPE,

                  amt_5=_AMT,
                  fund_5=_FUND,
                  type_5=_STYPE):
    # Generates a dummy row of PEP data that can be inserted into a PepRepo
    line = ' ' * 103  # Start with all blanks of appropriate length
    line = str_insert(line, ssn, 20)
    line = str_insert(line, obj_code, 37)
    line = str_insert(line, func_code, 40)
    # Salary data is repeated 5 times for each 200 rec: (amount, fund, type)
    line = str_insert(line, amt_1, 58)
    line = str_insert(line, fund_1, 64)
    line = str_insert(line, type_1, 66)

    line = str_insert(line, amt_2, 67)
    line = str_insert(line, fund_2, 73)
    line = str_insert(line, type_2, 75)

    line = str_insert(line, amt_3, 76)
    line = str_insert(line, fund_3, 82)
    line = str_insert(line, type_3, 84)

    line = str_insert(line, amt_4, 85)
    line = str_insert(line, fund_4, 91)
    line = str_insert(line, type_4, 93)

    line = str_insert(line, amt_5, 94)
    line = str_insert(line, fund_5, 100)
    line = str_insert(line, type_5, 102)

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


class TestSalaryOccs(unittest.TestCase):
    def test_assert(self):
        # No salary occs generated for zero amounts
        rec = dummy_pep_200()
        found = generate_salary_occs(rec)
        self.assertFalse(found)

        # Test single entries for each possible spot in the 200 rec
        nonzero_amt = '123456'
        nonzero_amt_int = int(nonzero_amt)

        rec1 = dummy_pep_200(amt_1=nonzero_amt)
        found = generate_salary_occs(rec1)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].amount, nonzero_amt_int)

        rec2 = dummy_pep_200(amt_2=nonzero_amt)
        found = generate_salary_occs(rec2)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].amount, nonzero_amt_int)

        rec3 = dummy_pep_200(amt_3=nonzero_amt)
        found = generate_salary_occs(rec3)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].amount, nonzero_amt_int)

        rec4 = dummy_pep_200(amt_4=nonzero_amt)
        found = generate_salary_occs(rec4)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].amount, nonzero_amt_int)

        rec5 = dummy_pep_200(amt_5=nonzero_amt)
        found = generate_salary_occs(rec5)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].amount, nonzero_amt_int)

        # Multiple amounts
        rec12 = dummy_pep_200(amt_1=nonzero_amt, amt_2=nonzero_amt)
        found = generate_salary_occs(rec12)
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0].amount, nonzero_amt_int)
        self.assertEqual(found[1].amount, nonzero_amt_int)

        # All possible amounts filled out
        rec12345 = dummy_pep_200(amt_1=nonzero_amt, amt_2=nonzero_amt,
            amt_3=nonzero_amt, amt_4=nonzero_amt, amt_5=nonzero_amt)
        found = generate_salary_occs(rec12345)
        self.assertEqual(len(found), 5)
        for i in range(5):
            self.assertEqual(found[i].amount, nonzero_amt_int)


class TestPepRepo(unittest.TestCase):
    def setUp(self):
        self.repo = PepRepo()
        self.repo.add_100(dummy_pep_100())
        self.repo.add_200(dummy_pep_200())

    def test_get_100(self):
        self.repo = PepRepo()
        rec = dummy_pep_100()
        self.repo.add_100(rec)
        found = self.repo.get_100(_SSN)
        self.assertEqual(found, rec)

    def test_get_200(self):
        self.repo = PepRepo()
        rec = dummy_pep_200()
        self.repo.add_200(rec)
        found = self.repo.get_200(_SSN)
        self.assertEqual(found, rec)

    def test_get_200s(self):
        self.repo = PepRepo()
        rec = dummy_pep_200()
        self.repo.add_200(rec)
        found = self.repo.get_200s(_SSN)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], rec)

        self.repo.add_200(rec)
        found = self.repo.get_200s(_SSN)
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0], rec)
        self.assertEqual(found[1], rec)

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

    def test_get_obj_code(self):
        self.assertEqual(_OBJ_CODE, self.repo.get_obj_code(_SSN))

    def test_get_func_code(self):
        self.assertEqual(_FUNC_CODE, self.repo.get_func_code(_SSN))

    def test_get_total_salary_amount(self):
        self.assertEqual(_TOTAL_SALARY_AMT_INT,
            self.repo.get_total_salary_amount(_SSN))


class TestPepSalaries(unittest.TestCase):
    def setUp(self):
        # Basic data pulls already covered, just testing sums/diffs here
        salary_100 = dummy_pep_100(pip_salary='000001', total_salary_amt='001111')
        salary_200_a = dummy_pep_200(
            amt_1='001000', fund_1='xx', type_1='1',
            amt_2='000100', fund_2='xx', type_2='2')
        salary_200_b = dummy_pep_200(
            amt_1='000010', fund_1='xx', type_1='x')
        self.repo = PepRepo()
        self.repo.add_100(salary_100)
        self.repo.add_200(salary_200_a)
        self.repo.add_200(salary_200_b)

    def test_get_all_occs(self):
        found = self.repo._get_all_occs(_SSN)
        self.assertEqual(len(found), 3)

    def test_get_extra_comp(self):
        found = self.repo.get_extra_compensation(_SSN)
        self.assertEqual(found, 110)

    def test_get_base_salary(self):
        found = self.repo.get_base_salary(_SSN)
        self.assertEqual(found, 1000)

    def test_get_total_salary(self):
        found = self.repo.get_total_salary_amount(_SSN)
        self.assertEqual(found, 1111)

    def test_validate_salary_sums(self):
        total_sal = self.repo.get_total_salary_amount(_SSN)
        pip_sal = self.repo.get_pip_salary(_SSN)
        extra_sal = self.repo.get_extra_compensation(_SSN)
        base_sal = self.repo.get_base_salary(_SSN)

        self.assertEqual(total_sal, 1111)
        self.assertEqual(base_sal, 1000)
        self.assertEqual(total_sal - pip_sal - extra_sal, base_sal)
