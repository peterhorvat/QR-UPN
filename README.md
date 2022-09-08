# QR UPN package

This is a small package that will generate a QR UPN.
The package also check the field length for each field and the validity of the field format.
This ensures that the generated QR code will be valid.

Feel free to address any issues or improvements.

---
Primer podatkov ki jih prejme funkcija _generate_, ki ustvari QR UPN dokument
```json
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
    'r_ref': 'SI06 125412-135-1257',
    'r_name': 'RentaCar d.o.o.',
    'r_address': 'Pohorska ulica 22',
    'r_post': '2000 Maribor'
}
```
