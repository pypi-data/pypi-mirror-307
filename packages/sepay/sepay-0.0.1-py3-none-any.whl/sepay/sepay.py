from sepay.bank_account import BankAccount
from sepay.transaction import Transaction

from .base import APIKey


class SePay(APIKey):
    def __init__(self, api_key: str):
        self.bank_account = BankAccount(api_key)
        self.transaction = Transaction(api_key)
