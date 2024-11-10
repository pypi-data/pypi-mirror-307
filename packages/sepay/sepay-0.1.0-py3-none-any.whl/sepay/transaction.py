from typing import Dict, List, Optional, TypeVar

from .base import BaseRequest
from .models import Transaction


class TransactionService(BaseRequest):
    def get_transactions(self, filters: Optional[Dict[str, str]] = None) -> List[Transaction]:
        """
        Example usage:

        ```python
        filters = {
            "account_number": "123456789",
            "transaction_date_min": "2023-01-01",
            "amount_in": "100.00"
        }
        transactions = transactions.get_transactions(filters=filters)
        ```

        Retrieve a list of transactions. You can filter the results using the following parameters
        either directly as method arguments or through the `filters` dictionary:

        - **account_number**:
        The bank account number to filter transactions.

        - **transaction_date_min**:
        Show transactions created on or after this date (>=). Format: `yyyy-mm-dd`.

        - **transaction_date_max**:
        Show transactions created on or before this date (<=). Format: `yyyy-mm-dd`.

        - **since_id**:
        Show transactions starting from the specified ID (>=).

        - **limit**:
        Limit the number of transactions returned. Maximum is 5000, default is 5000.

        - **reference_number**:
        Retrieve transactions matching the specified reference number.

        - **amount_in**:
        Retrieve incoming transactions that match this amount.

        - **amount_out**:
        Retrieve outgoing transactions that match this amount.

        The `filters` dictionary can include any of the parameters listed above. You can use either
        individual parameters or the `filters` dictionary to customize your query.
        """

        path = "transactions/list"
        params = filters or {}

        data = self._get(path, params=params)
        transactions = data.get("transactions", [])

        return [self.get_object(Transaction, transaction) for transaction in transactions]

    def get_transaction(self, transaction_id: str) -> Transaction:
        """
        Returns the details of a transaction_id.
        """
        path = "transactions/details/{}".format(transaction_id)
        data = self._get(path)

        return self.get_object(Transaction, data["transaction"])

    def get_count(self, filters: Optional[Dict[str, str]] = None) -> int:
        """
        Example usage:

        ```python
        filters = {
            "account_number": "123456789",
            "transaction_date_min": "2023-01-01",
            "transaction_date_max": "2023-12-31",
            "since_id": "1000"
        }
        transaction_count = transactions.get_count(filters=filters)
        ```

        Retrieve the count of transactions based on the specified filters. You can filter the results
        using the `filters` dictionary, which can include the following parameters:

        - **account_number**:
        The bank account number to filter transactions.

        - **transaction_date_min**:
        Show transactions created on or after this date (>=). Format: `yyyy-mm-dd`.

        - **transaction_date_max**:
        Show transactions created on or before this date (<=). Format: `yyyy-mm-dd`.

        - **since_id**:
        Show transactions starting from the specified ID (>=).

        The `filters` dictionary allows you to customize your query by including any combination
        of the parameters listed above.
        """
        path = "transactions/count"
        params = filters or {}

        data = self._get(path, params=params)

        return data["count_transactions"]
