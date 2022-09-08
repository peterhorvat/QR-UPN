import os
import re
import datetime
import locale
import segno
import string

from PIL import Image, ImageDraw, ImageFont
from schwifty import IBAN
from pandas import read_csv
from .rules import model_rules

locale.setlocale(locale.LC_ALL, 'sl_SI')
DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def check_name(name):
    if not name.endswitht('.png') or not name.endswitht('.jpg') or not name.endswitht('.jpeg'):
        return f"{name}.png"
    return name


def clean_str(s):
    return re.sub(r'[\n\t\s]*', '', s)


def get_font(style=os.path.join(DIR_PATH, 'courbd.ttf'), size=19):
    return ImageFont.truetype(style, size)


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


def control_number(column):
    ponders = [i for i in range(len([*column]) + 1, 1, -1)]
    result = 11 - (sum([a * b for a, b in zip(map(int, [*column]), ponders)]) % 11)
    if result == 10:
        return 0
    return result


def sum_multi(column):
    ponders = [i for i in range(len([*column]) + 1, 1, -1)]
    return sum([a * b for a, b in zip(map(int, [*column]), ponders)])


def model11_checksum(columns):
    last = int(columns[-1])
    result = 11 - (sum_multi(columns[:-1]) % 11)
    if result == 10 or result == 11:
        result = 0
    return result == last


def SI_model_check(ref):
    ref = clean_str(ref)
    columns = ref.split('-')
    _model = columns[0][2:4]
    columns[0] = columns[0][4:]
    try:
        columns = list(filter(lambda c: c != '', columns))
    except ValueError:
        pass

    # Same rules are included in CSV format in the rules.csv file

    model = model_rules.get(_model)

    # Check model 99
    if _model == '99':
        if len(ref) != 4:
            print(ValueError(f'Model 99 requires empty reference number'))
            return False
        else:
            return True

    # Check if enough columns
    if len(columns) < len([v for k, v in model.items() if 'part' in k and v.get('required')]):
        print(ValueError(f'Required columns are not set.'))
        return False

    # Check column lengths P1 - P2 - P3
    for inx, col in enumerate(columns):
        condition = f"{len(col)}{model.get(f'part{inx + 1}').get('condition')}"
        if not eval(condition):
            print(ValueError(f'Column length of reference is not valid for column {inx+1}: "{col}" ({condition}).'))
            return False

    # Check model 11 checksum
    single_controls = [i for i, ltr in enumerate(model.get('control')) if ltr == '1']
    combined_controls = [i for i, ltr in enumerate(model.get('control')) if ltr == '2']
    for i in single_controls:
        if i == 3:
            col_data = ''.join(columns)
        else:
            col_data = columns[i]
        if not model11_checksum(col_data):
            print(ValueError(f'Control number is not valid'))
            return False
    if len(combined_controls):
        i1, i2 = combined_controls
        col_data = ''.join(columns[i1:i2 + 1])
        if not model11_checksum(col_data):
            print(ValueError(f'Control number is not valid'))
            return False
    return True


def RF_model_check(ref):
    ref = clean_str(ref)
    checksum = ref[2:4]
    _ref = ref[4:]
    chars = [c for c in string.ascii_uppercase]
    c_i_dict = dict(zip(chars, range(10, len(chars) + 11)))
    remainder = int(''.join(list(map(lambda x: x if x.isnumeric() else str(c_i_dict.get(x)), f"{_ref}RF00")))) % 97
    result = str(98 - remainder)
    if int(result) < 10:
        result = f"0{result}"
    return checksum == result


def validate_reference(ref):
    ref = clean_str(ref)
    # General check if prefix, length and number of '-' is correct
    if re.compile('^(SI(0[0-9]|1(0|1|2|8|9)|(2|3)(1|8)|4(0|1|8|9)|5(1|5|8)|99)[0-9\-]{0,22}|RF[0-9]{2}[a-zA-Z0-9]{0,21})').match(ref) and ref.count('-') <= 2:
        if ref[:2] == 'SI':
            return SI_model_check(ref)
        else:
            return RF_model_check(ref)
    return False


def format_reference(ref):
    ref = clean_str(ref)
    if validate_reference(ref):
        return [ref[:4], ref[4:]]
    else:
        raise Exception('Reference is not in a valid format.')


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


def format_code(code):
    try:
        valid_codes = read_csv(os.path.join(DIR_PATH, 'codes.csv')).get('Koda').tolist()
        format_length(code, field_name='Purpose code', min_length=4, max_length=4)
        u_code = code.upper()
        if u_code in valid_codes:
            return u_code
        raise ValueError('Purpose code is not valid.')
    except Exception as e:
        raise Exception(repr(e))


def gen_qr_upn(p_name, p_address, p_post,
               r_iban, r_ref, r_name, r_address, r_post,
               price, date, purpose_code, purpose, pay_date,
               save_to=None, save_qr=None, show=False):
    img = Image.open(os.path.join(DIR_PATH, 'upn_sl.png'))
    kwargsL = {'font': get_font(), 'fill': (0, 0, 0)}
    kwargsS = {'font': get_font(size=15), 'fill': (0, 0, 0)}

    try:
        image = ImageDraw.Draw(img)

        # Format and validate data
        _r_iban = format_iban(r_iban)
        _r_ref = format_reference(r_ref)
        _r_name = format_length(r_name)
        _r_address = format_length(r_address)
        _r_post = format_length(r_post)
        _purpose_code = format_code(purpose_code)

        # Payer
        image.text((700, 155), format_length(p_name), **kwargsL)
        image.text((700, 187), format_length(p_address), **kwargsL)
        image.text((700, 219), format_length(p_post), **kwargsL)
        image.text((750, 270), format_price(price), **kwargsL)
        image.text((1055, 270), format_date(date), **kwargsL)

        image.text((420, 325), _purpose_code, **kwargsL)
        image.text((530, 325), format_length(purpose), **kwargsL)
        image.text((1155, 325), format_date(pay_date), **kwargsL)

        # Receiver
        image.text((420, 383), _r_iban, **kwargsL)
        image.text((420, 433), _r_ref[0], **kwargsL)
        image.text((535, 433), _r_ref[1], **kwargsL)

        image.text((420, 490), _r_name, **kwargsL)
        image.text((420, 522), _r_address, **kwargsL)
        image.text((420, 554), _r_post, **kwargsL)

        # Payer - ticket data
        image.text((35, 50), format_length(p_name), **kwargsS)
        image.text((35, 70), format_length(p_address), **kwargsS)
        image.text((35, 90), format_length(p_post), **kwargsS)

        image.text((35, 155), format_length(purpose, max_length=42), **kwargsS)
        image.text((35, 175), format_date(pay_date), **kwargsS)

        # Receiver - ticket data
        image.text((110, 230), format_price(price), **kwargsS)

        image.text((35, 290), _r_iban, **kwargsS)
        image.text((35, 330), format_length(r_ref[0], min_length=4, max_length=4), **kwargsS)
        image.text((80, 330), format_length(r_ref[1], max_length=22), **kwargsS)

        image.text((35, 390), _r_name, **kwargsS)
        image.text((35, 410), _r_address, **kwargsS)
        image.text((35, 430), _r_post, **kwargsS)

        # Generate QR code
        try:
            content = format(f'UPNQR\n\n\n\n\n{p_name}\n{p_address}\n{p_post}\n{format_price(price, qr=True)}\n\n\n'
                             f'{_purpose_code}\n{purpose}\n{pay_date}\n{r_iban}\n{"".join(_r_ref)}\n{r_name}\n{r_address}\n{r_post}')

            content = f'{content}\n{len(content)+1}\n'
            content = content.encode('iso-8859-2')

            qr = segno.make(
                content,
                version=15,
                mode='byte',
                error='M', boost_error=False,
                encoding='iso-8859-2', eci=True).to_pil().resize((230, 230))
            if save_qr: qr.save(check_name(save_qr))

            img.paste(qr, (427, 51))

            if save_to: img.save(check_name(save_to))
            if show: img.show()
        except Exception as e:
            raise Exception(repr(e))
        return img
    except Exception as e:
        raise repr(e)
