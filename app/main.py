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

@app.get("/get-revenue")
async def get_revenue():
    response = get_all_revenues()
    return response

@app.get("/get-expenses")
async def get_expenses():
    response = get_all_expenses()
    return response

@app.get("/revenue-expenses")
async def revenue_expenses():
    total_revenues = sum(item['value'] for item in get_all_revenues())
    total_expenses = sum(item['value'] for item in get_all_expenses())
    return total_revenues - total_expenses

@app.get("/expenses-by-category")
async def expenses_by_category(category: str):
    response = get_expenses_by_category(category)
    return response
    
