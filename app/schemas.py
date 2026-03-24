from pydantic import BaseModel, Field, model_validator
from typing import Literal
from datetime import date

class Item(BaseModel):
    value: float = Field(gt=0)
    type: str = Literal["receita", "despesa"]
    category: str = Field(min_length=1, max_length=100)
    date_item: date

class User(BaseModel):
    email: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise UserException('As senhas não coincidem.')
        return self

class UserException(Exception):
    pass