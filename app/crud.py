from fastapi import HTTPException
from database import supabase_connection as db
from schemas import Item
import calendar

def insert_item(item: dict):
    try:
        item['date_item'] = item['date_item'].isoformat()
        if item["type"] not in ["receita", "despesa"]:
            return "Invalid type. Must be 'receita' or 'despesa'."
        response = db.table("finance").insert(item).execute()
        return f"Item inserted successfully {response.data}"
    except Exception as e:
        return f"Error inserting item: {str(e)}"

def get_all_items(user_id):
    response = (
        db.table("finance")
        .select("*")
        .eq('user_id', user_id)
        .order("id", desc=True)
        .execute()
    )
    return response.data

def get_all_expense_incomes(type: str, user_id: str):
    response = (
        db.table("finance")
        .select("*")
        .eq('user_id', user_id)
        .eq("type", type)
        .execute()
    )
    return response.data

def get_expenses_income_by_category(type: str, category: str, user_id: str):
    query = db.table("finance").select("*").eq('user_id', user_id).eq("type", type)
    if category:
        query.eq("category", category)
    response = query.execute()
    return response.data

def delete_item(item_id: int, user_id: str):
    response = (
        db.table("finance")
        .delete()
        .eq('user_id', user_id)
        .eq("id", item_id)
        .execute()
    )
    if not response.data:
        raise PermissionDeniedError('No data')
    return f"Item with id {item_id} deleted successfully. {response.data}"

def update_item(item_id: int, item: Item, user_id: str):
    item_json = item.model_dump(mode="json")
    if item_json["type"] not in ["receita", "despesa"]:
            return "Invalid type. Must be 'receita' or 'despesa'."
    response = (
        db.table("finance")
        .update(item_json)
        .eq("id", item_id)
        .eq('user_id', user_id)
        .execute()
    )
    if not response.data:
        raise PermissionDeniedError('No data')
    return response.data

def get_by_month(type: str, month: int, year: int, user_id: str):
    last_day = calendar.monthrange(year, month)[1]
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{last_day}"
    response = (
         db.table("finance")
        .select("*")
        .eq("user_id", user_id)
        .eq("type", type)
        .gte("date_item", start_date)
        .lte("date_item", end_date)
        .execute()
    )
    return response.data

class PermissionDeniedError(Exception):
    pass