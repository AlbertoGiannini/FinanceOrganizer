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

def get_all_expense_revenues(type: str):
    response = (
        db.table("finance")
        .select("*")
        .eq("type", type)
        .execute()
    )
    return response.data

def get_expenses_revenue_by_category(type: str, category: str, ):
    query = db.table("finance").select("*").eq("type", type)
    if category:
        query.eq("category", category)
    response = query.execute()
    return response.data

def delete_item(item_id: int):
    response = (
        db.table("finance")
        .delete()
        .eq("id", item_id)
        .execute()
    )
    return f"Item with id {item_id} deleted successfully. {response.data}" 