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
        return response.data
    except Exception as e:
        print(e)
        return None

def get_all_items(user_id):
    try:
        response = (
            db.table("finance")
            .select("*, category(name)")
            .eq('user_id', user_id)
            .order("id", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        print(e)
        return None

def get_all_expense_incomes(type: str, user_id: str):
    try:
        response = (
            db.table("finance")
            .select("*")
            .eq('user_id', user_id)
            .eq("type", type)
            .execute()
        )
        return response.data
    except Exception as e:
        print(e)
        return None

def get_expenses_income_by_category(type: str, category: str, user_id: str):
    try:
        query = db.table("finance").select("*").eq('user_id', user_id).eq("type", type)
        if category:
            query.eq("category", category)
        response = query.execute()
        return response.data
    except Exception as e:
        print(e)
        return None

def delete_item(item_id: int, user_id: str):
    try:
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
    except Exception as e:
        print(e)
        return None

def update_item(item_id: int, item: Item, user_id: str):
    try:
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
    except Exception as e:
        print(e)
        return None
    except PermissionDeniedError as err:
        raise PermissionDeniedError(str(err))

def get_by_month(type: str, month: int, year: int, user_id: str):
    try:
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
    except Exception as e:
        print(e)
        return None

def get_total_amount(user_id: str):
    try:
        response = db.rpc("get_user_totals", {"p_user_id": user_id}).execute()
        return response.data
    except Exception as e:
        print(e)
        return None

def get_all_categories(user_id: str):
    try:
        response = (
            db.table("category")
            .select("*")
            .or_(f"user_id.is.null,user_id.eq.{user_id}")
            .execute()
        )
        return response.data
    except Exception as e:
        print(e)
        return None

def get_category_by_id(category_id: str):
    try:
        response = (
            db.table('category')
            .select('name')
            .eq('id', category_id)
            .execute()
        )
        return response.data

    except Exception as err:
        print(err)
        return None

class PermissionDeniedError(Exception):
    pass