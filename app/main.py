from typing import Literal
from fastapi import FastAPI
from schemas import Item
from crud import *

app = FastAPI()


@app.get("/get_all")
async def teste():
    response = get_all_items()
    return response

@app.post("/send-item")
async def send_item(item: Item):
    response = insert_item(item)
    return response

@app.get("/get-revenue-expenses")
async def get_revenue_expenses(type: Literal["receita", "despesa"]):
    response = get_all_expense_revenues(type)
    return response

@app.get("/total-amount")
async def total_amount():
    items = get_all_items()
    total_revenues = sum(item['value'] for item in items if item['type'] == "receita")
    total_expenses = sum(item['value'] for item in items if item['type'] == "despesa")
    return {
        "total_revenues": total_revenues,
        "total_expenses": total_expenses,
        "total-amount": total_revenues - total_expenses
    }

@app.get("/revenue-expenses-by-category")
async def revenue_expenses_by_category(type: str, category: str = None):
    response = get_expenses_revenue_by_category(type, category)
    return response

@app.delete("/delete-item/{item_id}")
async def remove_item(item_id: int):
    response = delete_item(item_id)
    return response
