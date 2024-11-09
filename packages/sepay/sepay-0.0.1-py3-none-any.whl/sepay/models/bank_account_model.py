from datetime import datetime

from pydantic import BaseModel, field_validator


class BankAccountModel(BaseModel):
    id: str
    account_holder_name: str
    account_number: str
    accumulated: str
    last_transaction: datetime
    label: str
    active: str
    created_at: datetime
    bank_short_name: str
    bank_full_name: str
    bank_bin: str
    bank_code: str

    # @field_validator('active', pre=True)
    # def convert_active(cls, value):
    #     return value == "1"

    @field_validator("active")
    @classmethod
    def to_bool(cls, v: str) -> bool:
        return v == "1"

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
