# Unofficial SePay SDK for Python

[![pypi](https://img.shields.io/pypi/v/sepay.svg)](https://pypi.org/project/sepay/)
[![python](https://img.shields.io/pypi/pyversions/sepay.svg)](https://pypi.org/project/sepay/)
[![Build Status](https://github.com/shinxz12/sepay/actions/workflows/dev.yml/badge.svg)](https://github.com/shinxz12/sepay/actions/workflows/dev.yml)


SDK for SePay API read more in [official docs](https://docs.sepay.vn/)

* Documentation: <https://shinxz12.github.io/sepay>
* GitHub: <https://github.com/shinxz12/sepay>
* PyPI: <https://pypi.org/project/sepay/>
* Free software: MIT

## Features

* Transaction APIs.
* Bank Account APIs.

## Example
* Create your API Key [here](https://my.sepay.vn/companyapi)
* Get data:
```
from sepay import SePay


se_pay = SePay(api_key=<YOUR_API_KEY>)
bank_account = se_pay.bank_account
transaction = se_pay.transaction

# Get transactions list with filters
transaction.get_transactions(filters={ "reference_number": 'FT24314R7N9P'})

# Get transactions count
transaction.get_count(filters={ "reference_number": 'FT24314R7'})

# Get transaction detail
transaction.get_transaction("4508999")

# Get bank accounts list
bank_account.get_bank_accounts(filters={ "reference_number": 'FT24314R7N9P'})

# Get bank accounts count
bank_account.get_count(filters={ "reference_number": 'FT24314R7'})

# Get bank account detail
bank_account.get_bank_account("3992")
```
