// const API_URL = "https://myfinancesaver.vercel.app/items";
const API_URL = "http://127.0.0.1:8000/items";

async function loadData() {
    try {
        const response = await fetch(`${API_URL}/get_all`);
        const data = await response.json();
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = "";
        data.forEach(item => {
            const line = document.createElement("tr");
            line.setAttribute("id", item.id);
            const valueColor = item.type === 'receita' ? 'green' : 'red';
            const date_item = item.date_item.split('-').reverse().join('/'); 
            line.innerHTML = `
                <td data-label="Descrição">${item.category}</td>
                <td data-label="Valor" style="color: ${valueColor};">R$ ${item.value}</td>
                <td data-label="Tipo">${item.type}</td>
                <td data-label="Data">${date_item}</td>
                <td data-label="Ações">
                    <button class="edit-button">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </button>
                    <button class="delete-button">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(line);
        });
        tableButtons();
    } catch (error) {
        console.error("Erro ao carregar os dados:", error);
    }
}

loadData();

async function loadAmount() {
    try {
        const response = await fetch(`${API_URL}/total-amount`);
        const data = await response.json();
        const amountElement = document.getElementById("current-balance");
        amountElement.textContent = `Saldo Atual: R$ ${data["total-amount"].toFixed(2)}`;
    } catch (error) {
        console.error("Erro ao carregar o saldo:", error);
    }
}

loadAmount();

const form = document.getElementById("transaction-form");
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const value = parseFloat(document.getElementById("amount").value);
    const type = document.getElementById("type").value;
    const category = document.getElementById("category").value;
    const date = document.getElementById("date").value;

    const newTransaction = {
        category: category,
        value: value,
        type: type,
        date_item: date
    };
    try {
        const response = await fetch(`${API_URL}/send-item`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newTransaction)
        });
        if (response.ok) {
            alert("Item adicionado com sucesso!");
            form.reset();
            loadData();
            loadAmount();
            loadMonthlyExpensesIncomes();
        } else {
            alert("Erro ao adicionar o item. Por favor, tente novamente.");
        }
        } catch (error) {
            console.error("Erro ao enviar o item:", error);
            alert("Erro ao enviar o item. Por favor, tente novamente.");
        }
});

async function tableButtons() {
    const tableBody = document.querySelectorAll("#transactions-table tr");
    tableBody.forEach(element => {
        const deleteButton = element.querySelector(".delete-button");
        const updateButton = element.querySelector(".edit-button");
        const id = element.id;
        if (deleteButton) {
            deleteButton.addEventListener("click", async function(event) {
            if (id) {
                await deleteItem(id);
                loadData();
                loadAmount();
                loadMonthlyExpensesIncomes();
                
            }
        });
        }
        if (updateButton) {
            updateButton.addEventListener("click", async function(event) {
            await editLine(id);
            
        });
        }
    });
}

function editLine(id) {
    const line = document.querySelector(`tr[id="${id}"]`);
    const columns = line.querySelectorAll("td")
    const oldCategory = columns[0].textContent;
    var oldValue = columns[1].textContent;
    oldValue = oldValue.replace("R$ ", "");
    oldValue = parseFloat(oldValue)
    const oldType = columns[2].textContent;
    const oldDate = columns[3].textContent;
    const oldDateFormatted = oldDate.split('/').reverse().join('-')

    line.innerHTML = `
        <td><input type="text" id="edit-cat-${id}" value="${oldCategory}" class="form-control"></td>
        <td><input type="number" id="edit-val-${id}" value="${oldValue}" class="form-control"></td>
        <td>
            <select id="edit-type-${id}" class="form-control">
                <option value="receita" ${oldType === 'receita' ? 'selected' : ''}>Receita</option>
                <option value="despesa" ${oldType === 'despesa' ? 'selected' : ''}>Despesa</option>
            </select>
        </td>
        <td><input type="date" id="edit-date-${id}" value="${oldDateFormatted}" class="form-control"></td>
        <td>
            <button onclick="updateItem(${id})" class="btn-save">✅</button>
            <button onclick="loadData()" class="btn-cancel">❌</button>
        </td>
    `;

}

async function deleteItem(id) {
    if (!confirm("Tem certeza que deseja excluir este item?")) {
        return;
    }
    try {
        const response = await fetch(`${API_URL}/delete-item/${id}`, {
            method: "DELETE"
        });
        if (response.status === 204) {
            loadAmount();
            loadData();
        } else {
            alert("Erro ao deletar o item. Por favor, tente novamente.");
        
        }
    } catch (error) {
        console.error("Erro ao deletar o item:", error);
        alert("Erro ao deletar o item. Por favor, tente novamente.");
    }
}

async function updateItem(id) {
    const payload = {
        category: document.getElementById(`edit-cat-${id}`).value,
        value: parseFloat(document.getElementById(`edit-val-${id}`).value),
        type: document.getElementById(`edit-type-${id}`).value,
        date_item: document.getElementById(`edit-date-${id}`).value
    };
    try {
        const response = await fetch(`${API_URL}/update-item/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.status === 204) {
            loadAmount();
            loadData();
            loadMonthlyExpensesIncomes();
        } else {
            alert("Erro ao editar o item. Por favor, tente novamente.");
        
        }
    } catch (error) {
        console.error("Erro ao editar o item:", error);
        alert("Erro ao editar o item. Por favor, tente novamente.");
    }
}

async function loadMonthlyExpensesIncomes() {
    expenseElement = document.getElementById("expense-month");
    incomeElement = document.getElementById("income");
    try {
        const [resRec, resDes] = await Promise.all([
            fetch(`${API_URL}/get-month-expenses?type=receita`),
            fetch(`${API_URL}/get-month-expenses?type=despesa`)
        ]);
        const receitas = await resRec.json();
        const despesas = await resDes.json();
        var totalIncomes = 0;
        receitas.forEach(item => {
            totalIncomes = totalIncomes + item['value'];
        });
        incomeElement.textContent = `R$ ${totalIncomes}`;

        var totalExpenses = 0;
        despesas.forEach(item => {
            totalExpenses = totalExpenses + item['value'];
        });
        expenseElement.textContent = `R$ ${totalExpenses}`;
    } catch (error) {
        console.error("Erro ao carregar os dados:", error);
    }
}

loadMonthlyExpensesIncomes();
