# QR UPN package

This is a small package that will generate a QR UPN.
The package also check the field length for each field and the validity of the field format.
This ensures that the generated QR code will be valid.
QR code validation checks were done using this [software](https://upn-qr.si/sl/preveriupnqr).

Feel free to address any issues or improvements.

---
## Functions:

### gen_qr_upn
This function create a UPN document with a valid QR code.
The parameters the function _requires_ are the following:
- **_p_name_**: Payer name
- **_p_address_**: Payer address
- **_p_post_**: Payer postal address and postal number
- **_price_**: Price the payer has to pay
- **_date_**: Date when the document is valid (DD.MM.YYYY)
- **_purpose_code_**: Purpose code which has to be valid (list of codes: [LINK](https://www.nlb.si/navodila-upn))
- **_purpose_**: Purpose of the payment
- **_pay_date_**: Date until the bill has to be paid (DD.MM.YYYY)
- **_r_iban_**: Receiver IBAN
- **_r_reference_**: Receiver reference (validated as mentioned: [LINK](https://www.upn-qr.si/uploads/files/NavodilaZaProgramerjeUPNQR.pdf))
- **_r_name_**: Receiver name
- **_r_address_**: Receiver address
- **_r_post_**: Receiver postal address and postal number

Optional parameters:
- **_save_to_**: Path where the QR UPN document will be saved to 
- **_save_qr_**: Path where the QR code will be saved to
- **_show_**: Visualize the generated QR UPN document


```python
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
        'r_post': '2000 Maribor',
        'save_to': './test.png',
        'save_qr': './test_qr.png',
        'show': True
    }
    gen_qr_upn(**data)
```

### validate_reference
Functions that checks if the provided reference code is valid.
It supports the SI and RF model.
The function accepts a single parameter:
```python
    validate_reference('SI02 5124123-62146-63720')
```

### SI_model_check
Function that handles the SI reference model validation.
```python
    SI_model_check('SI02 5124123-62146-63720')
```

### RF_model_check
Function that handles the RF reference model validation.
```python
    RF_model_check('SI02 5124123-62146-63720')
```