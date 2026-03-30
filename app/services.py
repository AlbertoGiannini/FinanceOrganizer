from crud import get_total_amount

def get_balance_oob(user_id):
    response = get_total_amount(user_id)
    html_oob = f"""
    <p id="current-balance" hx-swap-oob="true">R$ {response['total_amount']:.2f}</p>
    <p class="income-text" id="income" hx-swap-oob="true">R$ {response['total_incomes']:.2f}</p>
    <p class="expense-text" id="expense-month" hx-swap-oob="true">R$ {response['total_expenses']:.2f}</p>
    """
    return html_oob