from pydantic import BaseModel, Field
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
