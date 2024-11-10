from typing import Optional

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    bank_brand_name: str
    account_number: str
    transaction_date: str
    amount_out: str
    amount_in: str
    accumulated: str
    transaction_content: str
    reference_number: str
    code: Optional[str]
    sub_account: str
    bank_account_id: str
