import unittest
from src.qr_upn.generate import validate_reference, qr_upn


# PASSED
class QR_UPN_all_models(unittest.TestCase):
    data = {
        'p_name': 'JANEZ NOVAK',
        'p_address': 'Dunajska ulica 1',
        'p_post': '1000 Ljubljana',
        'price': '100',
        'date': '25.04.2019',
        'purpose_code': 'SWSB',
        'purpose': 'Plačilo najemnine za marec 2019',
        'pay_date': '30.04.2019',
        'r_iban': 'SI56037210001000102',
        'r_ref': '',
        'r_name': 'RentaCar d.o.o.',
        'r_address': 'Pohorska ulica 22',
        'r_post': '2000 Maribor'
    }

    # PASSED - QR VALID
    def test_Model00(self):
        self.data['r_ref'] = 'SI00123456789012-45678901'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model01(self):
        self.data['r_ref'] = 'SI01 1-5-11'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model02(self):
        self.data['r_ref'] = 'SI02 5124123-62146-63720'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model03(self):
        self.data['r_ref'] = 'SI03 125121-621351040-61220'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model04(self):
        self.data['r_ref'] = 'SI04 215123123-521312-78'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model05(self):
        self.data['r_ref'] = 'SI05 2141256-15123-165162'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model06(self):
        self.data['r_ref'] = 'SI06 125412-135-1257'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model07(self):
        self.data['r_ref'] = 'SI07 1124-5169-761'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model08(self):
        self.data['r_ref'] = 'SI08 12561-7828-827320'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model09(self):
        self.data['r_ref'] = 'SI09 72182-238212'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model10(self):
        self.data['r_ref'] = 'SI10 126896-290-23440'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model11(self):
        self.data['r_ref'] = 'SI11 1637134-8233411-21'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model12(self):
        self.data['r_ref'] = 'SI12 1362687524218'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model18(self):
        self.data['r_ref'] = 'SI18 73474-2782642-1'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model19(self):
        self.data['r_ref'] = 'SI19 62682016-15261-721'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model21(self):
        self.data['r_ref'] = 'SI21 12456721-123'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model28(self):
        self.data['r_ref'] = 'SI28 12351-1235680-12358347'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model31(self):
        self.data['r_ref'] = 'SI31 72467878-123456789012'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model38(self):
        self.data['r_ref'] = 'SI38 125235569-123561329-6'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model40(self):
        self.data['r_ref'] = 'SI40 125235569-123561329-6'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model41(self):
        self.data['r_ref'] = 'SI41 125235569-123561329-6'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model48(self):
        self.data['r_ref'] = 'SI48 125235569-123561329-6'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model49(self):
        self.data['r_ref'] = 'SI49 125235569-123561329-6'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model51(self):
        self.data['r_ref'] = 'SI51 125235569-123561329'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model55(self):
        self.data['r_ref'] = 'SI55 125235569-123561329'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_Model58(self):
        self.data['r_ref'] = 'SI58 125235569-123561329'
        qr_upn(**self.data)
    # PASSED - QR VALID

    def test_Model99(self):
        self.data['r_ref'] = 'SI99'
        qr_upn(**self.data)

    # PASSED - QR VALID
    def test_ModelRF(self):
        self.data['r_ref'] = 'RF71 2348231'
        qr_upn(**self.data)


# PASSED
class Format_testing(unittest.TestCase):

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