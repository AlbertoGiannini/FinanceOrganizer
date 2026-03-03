from typing import Literal
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas import Item
from crud import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_all", status_code=status.HTTP_200_OK)
async def teste():
    response = get_all_items()
    return response

@app.post("/send-item", status_code=status.HTTP_201_CREATED)
async def send_item(item: Item):
    response = insert_item(item)
    return response

@app.get("/get-income-expenses", status_code=status.HTTP_200_OK)
async def get_income_expenses(type: Literal["receita", "despesa"]):
    response = get_all_expense_incomes(type)
    return response

@app.get("/total-amount", status_code=status.HTTP_200_OK)
async def total_amount():
    items = get_all_items()
    total_incomes = sum(item['value'] for item in items if item['type'] == "receita")
    total_expenses = sum(item['value'] for item in items if item['type'] == "despesa")
    return {
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "total-amount": total_incomes - total_expenses
    }

@app.get("/income-expenses-by-category", status_code=status.HTTP_200_OK)
async def income_expenses_by_category(type: str, category: str = None):
    response = get_expenses_income_by_category(type, category)
    return response

@app.delete("/delete-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(item_id: int):
    response = delete_item(item_id)
    return response
