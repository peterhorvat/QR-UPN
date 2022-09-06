import re
import datetime
import locale

import segno

import upnqr
from PIL import Image, ImageDraw, ImageFont
from schwifty import IBAN

locale.setlocale(locale.LC_ALL, 'sl_SI')


def get_font(style='courbd.ttf', size=19):
    return ImageFont.truetype(style, size)


def is_valid_length(field, field_name='Field', min_length=0, max_length=33):
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


def validate_reference(ref):
    general_rules = {
        'prefix': 4,
        'max_length': 20,
        'delimiter_count': 2,
        'delimiter': '-'
    }
    model_rules = {

        '00': {
            'control': '0000',
            'regex': '[0-9]{1,12}-{0,1}[0-9]{0,12}-{0,1}[0-9]{0,12}',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': False,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '01': {
            'control': '0001',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': False,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '02': {
            'control': '0110',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': True,
                'condition': '<=12'
            }
        },
        '03': {
            'control': '1110',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': True,
                'condition': '<=12'
            }
        },
        '04': {
            'control': '1010',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': True,
                'condition': '<=12'
            }
        },
        '05': {
            'control': '1000',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': False,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '06': {
            'control': '0220',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': True,
                'condition': '<=12'
            }
        },
        '07': {
            'control': '0100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '08': {
            'control': '2210',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '09': {
            'control': '2200',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': False,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '10': {
            'control': '1220',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '11': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '12': {
            'control': '1000',
            'part1': {
                'required': True,
                'condition': '<=13'
            },
            'part2': {
                'required': False,
                'condition': '=0'
            },
            'part3': {
                'required': False,
                'condition': '=0'
            }
        },
        '18': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '=5'
            },
            'part2': {
                'required': True,
                'condition': '=7'
            },
            'part3': {
                'required': False,
                'condition': '=8'
            }
        },
        '19': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '=8'
            },
            'part2': {
                'required': True,
                'condition': '=5'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '21': {
            'control': '1000',
            'part1': {
                'required': True,
                'condition': '=8'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '=0'
            }
        },
        '28': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '=5'
            },
            'part2': {
                'required': True,
                'condition': '=7'
            },
            'part3': {
                'required': False,
                'condition': '<=8'
            }
        },
        '31': {
            'control': '1000',
            'part1': {
                'required': True,
                'condition': '=8'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '=0'
            }
        },
        '38': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '40': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '41': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '48': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12>'
            }
        },
        '49': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '51': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '55': {
            'control': '1000',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': False,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '58': {
            'control': '1100',
            'part1': {
                'required': True,
                'condition': '<=12'
            },
            'part2': {
                'required': True,
                'condition': '<=12'
            },
            'part3': {
                'required': False,
                'condition': '<=12'
            }
        },
        '99': {
            'blank': True
        }
    }
    print(list(model_rules.keys()))
    prefix = ref[:2]
    model = ref[2:4]
    print(model_rules.get(model))

def format_reference(ref):
    validate_reference(ref)
    if re.compile("^(SI|RF){1}(0[0-9]{1}|1(0|1|2|8|9){1}|(2|3){1}(1|8){1}|4(0|1|8|9){1}|5(1|5|8){1}|99){1}[0-9]{0,20}").match(ref):
        return [ref[:4], ref[5:]]
    else:
        raise Exception("Reference is not in a valid format.")


def format_price(price, qr=False):
    if int(price) <= pow(10, 9) - 1:
        if isinstance(price, str):
            if re.compile("^\d+(\.\d{2})?$").match(price) or isinstance(price, (int, float)):
                _price = float(price)
                if qr:
                    return f"{'0'*(10-len(str(_price).replace('.','')))}{int(100*_price)}"
                return f'***{locale.format_string("%.2f", _price, True)}'
        else:
            raise TypeError('Incorrect price format')
    else:
        raise ValueError('Number is to large, maximum allowed size is 10^9 - 1')


def format_code(code):
    try:
        is_valid_length(code, field_name='Purpose code', min_length=4, max_length=4)
        return code.upper()
    except Exception as e:
        raise Exception(repr(e))


def qr_upn(p_name, p_address, p_post,
           r_iban, r_ref, r_name, r_address, r_post,
           price, date, purpose_code, purpose, pay_date,
           save_to=None):

    img = Image.open('upn_sl.png')
    kwargsL = {'font': get_font(), 'fill': (0, 0, 0)}
    kwargsS = {'font': get_font(size=15), 'fill': (0, 0, 0)}

    try:
        image = ImageDraw.Draw(img)

        # Format and validate data
        _r_iban = format_iban(r_iban)
        _r_ref = format_reference(r_ref)
        _r_name = is_valid_length(r_name)
        _r_address = is_valid_length(r_address)
        _r_post = is_valid_length(r_post)

        # Payer
        image.text((700, 155), is_valid_length(p_name), **kwargsL)
        image.text((700, 187), is_valid_length(p_address), **kwargsL)
        image.text((700, 219), is_valid_length(p_post), **kwargsL)
        image.text((750, 270), format_price(price), **kwargsL)
        image.text((1055, 270), format_date(date), **kwargsL)

        image.text((420, 325), is_valid_length(purpose_code), **kwargsL)
        image.text((530, 325), is_valid_length(purpose), **kwargsL)
        image.text((1155, 325), format_date(pay_date), **kwargsL)

        # Receiver
        image.text((420, 383), _r_iban, **kwargsL)
        image.text((420, 433), _r_ref[0], **kwargsL)
        image.text((535, 433), _r_ref[1], **kwargsL)

        image.text((420, 490), _r_name, **kwargsL)
        image.text((420, 522), _r_address, **kwargsL)
        image.text((420, 554), _r_post, **kwargsL)

        # Payer - ticket data
        image.text((35, 50), is_valid_length(p_name), **kwargsS)
        image.text((35, 70), is_valid_length(p_address), **kwargsS)
        image.text((35, 90), is_valid_length(p_post), **kwargsS)

        image.text((35, 155), is_valid_length(purpose, max_length=42), **kwargsS)
        image.text((35, 175), format_date(pay_date), **kwargsS)

        # Receiver - ticket data
        image.text((110, 230), format_price(price), **kwargsS)

        image.text((35, 290), _r_iban, **kwargsS)
        image.text((35, 330), is_valid_length(r_ref[0], min_length=4, max_length=4), **kwargsS)
        image.text((80, 330), is_valid_length(r_ref[1], max_length=22), **kwargsS)

        image.text((35, 390), _r_name, **kwargsS)
        image.text((35, 410), _r_address, **kwargsS)
        image.text((35, 430), _r_post, **kwargsS)

        # Generate QR code
        try:
            content = format(f'UPNQR\n\n\n\n\n{p_name}\n{p_address}\n{p_post}\n{format_price(price, qr=True)}\n\n\n'
                             f'{purpose_code}\n{purpose}\n{pay_date}\n{r_iban}\n{r_ref}\n{r_name}\n{r_address}\n{r_post}')

            content = f'{content}\n{len(content)}\n'
            content = content.encode('iso-8859-2')

            qr = segno.make(
                content,
                version=15,
                mode='byte',
                error='M', boost_error=False,
                encoding='iso-8859-2', eci=True)
            
            qr.to_pil().resize((300, 300)).save('test.png')
            img.paste(qr.to_pil().resize((230, 230)), (427, 51))
        except Exception as e:
            raise Exception(repr(e))

        if save_to:
            img.save(save_to)
        else:
            img.save(f'{r_name}_{r_ref[1]}.png')
        # img.show()
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':

    data = {
        'p_name': 'JANEZ NOVAK',
        'p_address': 'Dunajska ulica 1',
        'p_post': '1000 Ljubljana',
        'price': '100',
        'date': '25.04.2019',
        'purpose_code': 'RENT',
        'purpose': 'Plačilo najemnine za marec 2019',
        'pay_date': '30.04.2019',
        'r_iban': 'SI56037210001000102',
        'r_ref': 'SI1914788594-07129-0722',
        'r_name': 'RentaCar d.o.o.',
        'r_address': 'Pohorska ulica 22',
        'r_post': '2000 Maribor'
    }
    qr_upn(**data)
