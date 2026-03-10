from typing import Literal
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from schemas import Item
from crud import *
from auth import get_current_user

router = APIRouter(prefix="/items", tags=["Finance Transactions"])

@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all(current_user: dict = Depends(get_current_user)):
    response = get_all_items()
    return response

@router.post("/send-item", status_code=status.HTTP_201_CREATED)
async def send_item(item: Item, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    new_item = item.model_dump()
    new_item['user_id'] = user_id
    response = insert_item(new_item)
    return response

@router.get("/get-income-expenses", status_code=status.HTTP_200_OK)
async def get_income_expenses(type: Literal["receita", "despesa"], current_user: dict = Depends(get_current_user)):
    response = get_all_expense_incomes(type)
    return response

@router.get("/total-amount", status_code=status.HTTP_200_OK)
async def total_amount(current_user: dict = Depends(get_current_user)):
    items = get_all_items()
    total_incomes = sum(item['value'] for item in items if item['type'] == "receita")
    total_expenses = sum(item['value'] for item in items if item['type'] == "despesa")
    return {
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "total-amount": total_incomes - total_expenses
    }

@router.get("/income-expenses-by-category", status_code=status.HTTP_200_OK)
async def income_expenses_by_category(type: str, category: str = None, current_user: dict = Depends(get_current_user)):
    response = get_expenses_income_by_category(type, category)
    return response

@router.delete("/delete-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(item_id: int, current_user: dict = Depends(get_current_user)):
    response = delete_item(item_id)
    return response

@router.put("/update-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_item(item_id: int, item: Item, current_user: dict = Depends(get_current_user)):
    response = update_item(item_id, item)
    return response

@router.get("/get-month-expenses", status_code=status.HTTP_200_OK)
async def get_month_expenses(
        type: Literal["receita", "despesa"],
        month: int = datetime.now().month,
        year: int = datetime.now().year,
        current_user: dict = Depends(get_current_user)
    ):
    response = get_by_month(type, month, year)
    return response
