from typing import Dict, List, Optional

from .base import BaseRequest
from .models import BankAccountModel


class BankAccount(BaseRequest):
    def get_bank_accounts(
        self,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[BankAccountModel]:
        """
        Example usage:

        ```python
        filters = {
            "account_number": "123456789",
            "transaction_date_min": "2023-01-01",
            "amount_in": "100.00"
        }
        bank_accounts = bank_accounts.get_bank_accounts(filters=filters)
        ```

        Retrieve a list of bank_account. You can filter the results using the following parameters
        either directly as method arguments or through the `filters` dictionary:

        - **short_name**:
        The name of the bank (short name) to filter accounts.

        - **last_transaction_date_min**:
        Filter accounts with the most recent transaction date on or after this date (>=). Format: `yyyy-mm-dd`.

        - **last_transaction_date_max**:
        Filter accounts with the most recent transaction date on or before this date (<=). Format: `yyyy-mm-dd`.

        - **since_id**:
        Show bank accounts starting from the specified ID (>=).

        - **limit**:
        Limit the number of bank accounts returned. Defaults to 100.

        - **accumulated_min**:
        Filter bank accounts with a balance greater than or equal to this amount (>=).

        - **accumulated_max**:
        Filter bank accounts with a balance less than or equal to this amount (>=).

        The `filters` dictionary can include any of the parameters listed above. You can use either
        individual parameters or the `filters` dictionary to customize your query.
        """

        path = "bankaccounts/list"
        params = filters or {}

        data = self._get(path, params=params)
        bank_accounts = data.get("bankaccounts", [])

        return [self.get_object(BankAccountModel, transaction) for transaction in bank_accounts]

    def get_bank_account(self, transaction_id: str) -> BankAccountModel:
        """
        Returns the details of a transaction_id.
        """
        path = "bankaccounts/details/{}".format(transaction_id)
        data = self._get(path)

        return self.get_object(BankAccountModel, data["bankaccount"])

    def get_count(self, filters: Optional[Dict[str, str]] = None) -> int:
        """
        Example usage:

        ```python
        filters = {
            "since_id": "1000"
        }
        count = bank_account.get_count(filters=filters)
        ```

        Retrieve the count of bank_account based on the specified filters. You can filter the results
        using the `filters` dictionary, which can include the following parameters:

        - **short_name**:
        The name of the bank, corresponding to the short name field.

        - **last_transaction_date_min**:
        Filter accounts with the most recent transaction date on or after this date (>=). Format: `yyyy-mm-dd`.

        - **last_transaction_date_max**:
        Filter accounts with the most recent transaction date on or before this date (<=). Format: `yyyy-mm-dd`.

        - **since_id**:
        Show bank accounts starting from the specified ID (>=).

        - **accumulated_min**:
        Filter bank accounts with a balance greater than or equal to this amount (>=).

        - **accumulated_max**:
        Filter bank accounts with a balance less than or equal to this amount (<=).

        The `filters` dictionary allows you to customize your query by including any combination
        of the parameters listed above.
        """
        path = "bankaccounts/count"
        params = filters or {}

        data = self._get(path, params=params)

        return data["count_bankaccounts"]
