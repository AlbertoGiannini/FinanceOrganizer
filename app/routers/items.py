from typing import Literal
from fastapi import APIRouter, HTTPException, status, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from schemas import Item
from crud import *
from auth import get_current_user
from services import *

router = APIRouter(prefix="/items", tags=["Finance Transactions"])

templates = Jinja2Templates(directory="templates")

@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    response = get_all_items(user_id)
    return response

@router.post("/send-item", status_code=status.HTTP_200_OK)
async def send_item(
    request: Request,
    value: float = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    date_item: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        if value <= 0:
            raise HTTPException(status_code=400, detail="Value must be greater than zero.")
        user_id = current_user.get("sub")
        item = Item(value=value, type=type, category=category, date_item=date_item)
        new_item = item.model_dump()
        new_item['user_id'] = user_id
        response = insert_item(new_item)
        if not response:
            raise HTTPException(status_code=500, detail='Failed to insert item')
        new_item['id'] = response[0].get('id')
        amount = get_balance_oob(user_id)
        category = get_category_by_id(category)
        # Validade category[0]
        new_item['category'] = {'name': category[0].get('name')}
        item_html = templates.TemplateResponse(request, "item.html", context={"item": new_item, "amount_html": amount}).body.decode("utf-8")
        response_alert = show_alert("success", "Item adicionado com sucesso!")
        response_html = HTMLResponse(content=item_html)
        response_html.headers["HX-Trigger"] = response_alert
        return response_html

    except HTTPException as http_err:
        raise http_err

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/get-income-expenses", status_code=status.HTTP_200_OK)
async def get_income_expenses(type: Literal["receita", "despesa"], current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    response = get_all_expense_incomes(type, user_id)
    return response

@router.get("/total-amount", status_code=status.HTTP_200_OK)
async def total_amount(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    response = get_total_amount(user_id)
    return response

@router.get("/income-expenses-by-category", status_code=status.HTTP_200_OK)
async def income_expenses_by_category(type: str, category: str = None, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    response = get_expenses_income_by_category(type, category, user_id)
    return response

@router.delete("/delete-item/{item_id}", status_code=status.HTTP_200_OK)
async def remove_item(request: Request, item_id: int, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        response = delete_item(item_id, user_id)
        if not response:
            raise HTTPException(status_code=403, detail='Forbidden')
        response = get_balance_oob(user_id)
        response_alert = show_alert("success", "Item removido com sucesso!")
        response_html = HTMLResponse(content=response)
        response_html.headers["HX-Trigger"] = response_alert
        return response_html
    except PermissionDeniedError as err:
        raise HTTPException(status_code=403, detail=str(err))    

    except Exception as err:
        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.put("/update-item/{item_id}", status_code=status.HTTP_200_OK)
async def change_item(
    item_id: int,
    request: Request,
    value: float = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    date_item: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("sub")
        item = Item(value=value, type=type, category=category, date_item=date_item)
        response = update_item(item_id, item, user_id)
        if not response:
            raise HTTPException(status_code=403, detail='Forbidden')
        amount = get_balance_oob(user_id)
        new_item = item.model_dump()
        new_item['id'] = item_id
        category = get_category_by_id(category)
        # Validade category[0]
        new_item['category'] = {'name': category[0].get('name')}
        item_html = templates.TemplateResponse(request, "item.html", context={"item": new_item, "amount_html": amount}).body.decode("utf-8")
        response_alert = show_alert("success", "Item atualizado com sucesso!")
        response_html = HTMLResponse(content=item_html)
        response_html.headers["HX-Trigger"] = response_alert
        return response_html
    except PermissionDeniedError as err:
        raise HTTPException(status_code=403, detail=str(err))    

    except Exception as err:
        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.get("/get-month-expenses", status_code=status.HTTP_200_OK)
async def get_month_expenses(
        type: Literal["receita", "despesa"],
        month: int = datetime.now().month,
        year: int = datetime.now().year,
        current_user: dict = Depends(get_current_user)
    ):
    user_id = current_user.get("sub")
    response = get_by_month(type, month, year, user_id)
    return response

@router.get("/get-all-categories", status_code=status.HTTP_200_OK)
async def get_categories(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    response = get_all_categories(user_id)
    return response