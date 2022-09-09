import datetime
import locale
import os
import re

from pandas import read_csv
from schwifty import IBAN


def format_length(field, field_name='Field', min_length=0, max_length=33):
    if min_length <= len(field) > max_length:
        raise ValueError(f'{field_name} length must be more than {min_length} characters.')
    else:
        return field[:max_length]


def format_iban(iban):
    _iban = IBAN(iban, allow_invalid=True)
    if _iban.is_valid:
        return _iban.formatted
    else:
        raise ValueError('Provided IBAN number is not valid.')


def format_date(datum):
    try:
        datetime.datetime.strptime(datum, '%d.%m.%Y')
        return datum
    except ValueError:
        raise ValueError('Incorrect data format, should be DD.MM.YYYY')


def format_price(price, qr=False):
    if int(price) <= pow(10, 9) - 1:
        if isinstance(price, str):
            if re.compile("^\d+(\.\d{2})?$").match(price) or isinstance(price, (int, float)):
                _price = float(price)
                if qr:
                    return f'{"0" * (10 - len(str(_price).replace(".", "")))}{int(100 * _price)}'
                return f'***{locale.format_string("%.2f", _price, True)}'
        else:
            raise TypeError('Incorrect price format')
    else:
        raise ValueError('Number is to large, maximum allowed size is 10^9 - 1')


def format_code(code, codes=os.path.dirname(os.path.abspath(__file__))):
    try:
        valid_codes = read_csv(os.path.join(codes, 'codes.csv')).get('Koda').tolist()
        format_length(code, field_name='Purpose code', min_length=4, max_length=4)
        u_code = code.upper()
        if u_code in valid_codes:
            return u_code
        raise ValueError('Purpose code is not valid.')
    except Exception as e:
        raise Exception(repr(e))
