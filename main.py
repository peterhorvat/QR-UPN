from qr_upn.utils import gen_qr_upn

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
    'r_ref': 'SI03 125121-621351040-61220',
    'r_name': 'RentaCar d.o.o.',
    'r_address': 'Pohorska ulica 22',
    'r_post': '2000 Maribor',
    'save_to': './test',
    'save_qr': './test_Qr',
    'show': True
}

gen_qr_upn(**data)
