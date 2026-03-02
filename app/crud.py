from database import supabase_connection as db
from schemas import Item

def insert_item(item: Item):
    try:
        data = item.model_dump()
        data['date_item'] = item.date_item.isoformat()
        if data["type"] not in ["receita", "despesa"]:
            return "Invalid type. Must be 'receita' or 'despesa'."
        response = db.table("finance").insert(data).execute()
        return f"Item inserted successfully {response.data}"
    except Exception as e:
        return f"Error inserting item: {str(e)}"

def get_all_items():
    response = (
        db.table("finance")
        .select("*")
        .execute()
    )
    return response.data

def get_all_revenues():
    response = (
        db.table("finance")
        .select("*")
        .eq("type", "receita")
        .execute()
    )
    return response.data

def get_all_expenses():
    response = (
        db.table("finance")
        .select("*")
        .eq("type", "despesa")
        .execute()
    )
    return response.data

def get_expenses_by_category(category: str):
    response = (
        db.table("finance")
        .select("*")
        .eq("type", "despesa")
        .eq("category", category)
        .execute()
    )
    return response.data