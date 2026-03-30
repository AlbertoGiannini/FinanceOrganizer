
//API_URL = "https://myfinancesaver.vercel.app/items";
API_URL = "http://127.0.0.1:8000/items";

async function tableButtons() {
    const tableBody = document.querySelectorAll("#transactions-table tr");
    tableBody.forEach(element => {
        const updateButton = element.querySelector(".edit-button");
        const id = element.id;
        if (updateButton) {
            updateButton.addEventListener("click", async function (event) {
                await editLine(id);
            });
        }
    });
}

tableButtons();

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
            <button class="btn-cancel">❌</button>
        </td>
    `;

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
            window.location.reload();
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

//loadMonthlyExpensesIncomes();

const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
const mobileNav = document.querySelector('.mobile-nav');
const closeNavButton = document.querySelector('.close-nav-button');
const navLinks = document.querySelectorAll('.mobile-nav a');

function openNav() {
    mobileNav.classList.add('active');
    document.body.classList.add('mobile-nav-open');
}

function closeNav() {
    mobileNav.classList.remove('active');
    document.body.classList.remove('mobile-nav-open');
}

mobileNavToggle.addEventListener('click', openNav);
closeNavButton.addEventListener('click', closeNav);

navLinks.forEach(link => {
    link.addEventListener('click', closeNav);
});

document.addEventListener('click', (event) => {
    if (mobileNav.classList.contains('active') && !mobileNav.contains(event.target) && !mobileNavToggle.contains(event.target)) {
        closeNav();
    }
});


// --- INTERCEPTAÇÃO DE ALERTAS DE CONFIRMAÇÃO (SWEETALERT2) ---
document.body.addEventListener('htmx:confirm', function (e) {
    // Verifica se o elemento clicado tem o nosso atributo customizado
    if (e.detail.elt.hasAttribute('confirm-with-sweet-alert')) {

        // Pausa a requisição do HTMX
        e.preventDefault();

        // Chama o pop-up do SweetAlert2
        Swal.fire({
            title: 'Deletar este item?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Confirmar',
            cancelButtonText: 'Cancelar',
            width: '250px',        // Trava a largura máxima para não estourar na tela    // Diminui o espaço em branco dentro do alerta
            customClass: {
                title: 'swal-title-small', // (Opcional) Você pode criar essa classe no seu CSS se quiser diminuir mais a fonte
                actions: 'swal-actions-mobile'
            }
        }).then((result) => {
            if (result.isConfirmed) {
                // Libera o HTMX para enviar a requisição ao FastAPI
                e.detail.issueRequest(true);
            }
        });
    }
});
