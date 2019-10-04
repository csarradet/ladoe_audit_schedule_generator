import unittest
from pep_repo import PepRepo


def str_insert(original_str, new_text, starting_pos):
    return original_str[:starting_pos] + new_text + original_str[starting_pos + len(new_text):]


DUMMY_SSN = '000000001'
DUMMY_NAME = 'BOB' + (' ' * 50)


def dummy_pep_100(ssn=DUMMY_SSN,
                  name=DUMMY_NAME):
    # Generates a dummy row of PEP 100 data that can be inserted into a PepRepo
    line = " " * 188  # Start with all blanks of appropriate length
    line = str_insert(line, ssn, 20)
    line = str_insert(line, name, 29)
    return line


class TestUtils(unittest.TestCase):
    def test_str_insert(self):
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

    def test_get_name(self):
        self.repo.add_100(dummy_pep_100())
        found = self.repo.get_name(DUMMY_SSN)
        self.assertEqual(found, DUMMY_NAME)

    def test_get_100(self):
        rec = dummy_pep_100()
        self.repo.add_100(rec)
        found = self.repo.get_100(DUMMY_SSN)
        self.assertEqual(found, rec)
