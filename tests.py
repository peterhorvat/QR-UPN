import unittest
from main import validate_reference


class Model_00(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI00123456789012-45678901'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false(self):
        ref = 'SI00'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_invalid_format1(self):
        ref = 'SI00-'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_invalid_format2(self):
        ref = 'SI00--'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_invalid_format3(self):
        ref = 'SI00---'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_01(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI01 1412-5214-123140'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false1(self):
        ref = 'SI01 1412-5214'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false2(self):
        ref = 'SI01 1412'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false3(self):
        ref = 'SI01'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_02(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI02 5124123-62146-63720'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false1(self):
        ref = 'SI02 1241241-765481'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false2(self):
        ref = 'SI02 1241241'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false3(self):
        ref = 'SI02'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_03(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI03 1251236-6213510-6124216'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false1(self):
        ref = 'SI03 1251236-6213510'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false2(self):
        ref = 'SI03 1251236'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false3(self):
        ref = 'SI03'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_04(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI04 215123123-521312-78'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false1(self):
        ref = 'SI04 215123123-521312'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false2(self):
        ref = 'SI04 215123123'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false3(self):
        ref = 'SI04'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_05(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI05	2141256-15123-165162'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_true1(self):
        ref = 'SI05	2141256-15123'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_true2(self):
        ref = 'SI05	2141256'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false3(self):
        ref = 'SI05'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)


class Model_06(unittest.TestCase):

    def test_checksum(self):
        ref = 'SI06	15612431-111111-1111112'
        actual = validate_reference(ref)
        self.assertEqual(actual, True)

    def test_required_parts_false1(self):
        ref = 'SI06	15612431-16123'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false2(self):
        ref = 'SI06	15612431'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

    def test_required_parts_false3(self):
        ref = 'SI06'
        actual = validate_reference(ref)
        self.assertEqual(actual, False)

