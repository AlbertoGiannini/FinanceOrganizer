from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Literal
from datetime import date

class Item(BaseModel):
    value: float = Field(gt=0)
    type: str = Literal["receita", "despesa"]
    category: str = Field(min_length=1, max_length=100)
    date_item: date

class UserEmail(BaseModel):
    email: str

class UserLogin(UserEmail):
    password: str

class UserRegister(UserEmail):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise UserException('As senhas não coincidem.')
        return self

class UserException(Exception):
    pass