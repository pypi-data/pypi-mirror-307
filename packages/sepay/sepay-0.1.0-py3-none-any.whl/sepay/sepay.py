from sepay.bank_account import BankAccountService
from sepay.transaction import TransactionService

from .base import APIKey


class SePay(APIKey):
    def __init__(self, api_key: str):
        self.bank_account = BankAccountService(api_key)
        self.transaction = TransactionService(api_key)
