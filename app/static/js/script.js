
//API_URL = "https://myfinancesaver.vercel.app/items";
API_URL = "http://127.0.0.1:8000/items";

async function tableButtons() {
    const tableBody = document.querySelectorAll("#transactions-table tr");
    tableBody.forEach(element => {
        const updateButton = element.querySelector(".edit-button");
        const id = element.id;
        if (updateButton && !updateButton.dataset.bound) {
            updateButton.dataset.bound = "true";
            updateButton.addEventListener("click", async function (event) {
                await editLine(id);
            });
        }
    });
}

tableButtons();

// Adicionamos isso para garantir que toda vez que o HTMX trouxer uma linha nova do servidor
// ele re-ative o botão de editar apenas dessa linha nova, sem duplicar os antigos!
document.body.addEventListener('htmx:afterSwap', function(evt) {
    tableButtons();
});

const originalRows = {};

function editLine(id) {
    const line = document.querySelector(`tr[id="${id}"]`);
    if (!originalRows[id]) {
        originalRows[id] = line.innerHTML;
    }
    const select_categories = document.getElementById('category');
    const select_options = select_categories.innerHTML;
    const columns = line.querySelectorAll("td");
    const oldCategory = columns[0].textContent;
    var oldValue = columns[1].textContent;
    oldValue = oldValue.replace("R$ ", "");
    oldValue = parseFloat(oldValue)
    const oldType = columns[2].textContent;
    const oldDate = columns[3].textContent;
    const oldDateFormatted = oldDate.split('/').reverse().join('-')

    line.innerHTML = `
        <td><select id="edit-cat-${id}" name="category" class="form-control">
                ${select_options}
            </select>
        <td><input type="number" id="edit-val-${id}" name="value" value="${oldValue}" class="form-control"></td>
        <td>
            <select id="edit-type-${id}" name="type" class="form-control">
                <option value="receita" ${oldType === 'receita' ? 'selected' : ''}>Receita</option>
                <option value="despesa" ${oldType === 'despesa' ? 'selected' : ''}>Despesa</option>
            </select>
        </td>
        <td><input type="date" id="edit-date-${id}" name="date_item" value="${oldDateFormatted}" class="form-control"></td>
        <td>
            <button type="button" 
            hx-put="/items/update-item/${id}" 
            hx-include="closest tr" 
            hx-target="closest tr" 
            hx-swap="outerHTML" 
            class="btn-save">✅
            </button>
            <button type="button" class="btn-cancel" onclick="cancelEdit('${id}')">❌</button>
        </td>
    `;
    const selectEdit = document.getElementById(`edit-cat-${id}`);
    selectEdit.querySelector('option[value=""]').remove()
    Array.from(selectEdit.options).forEach(option => {
        if (option.text.trim() === oldCategory.trim()) {
            option.selected = true;
        }
    });
    htmx.process(line);
}

function cancelEdit(id) {
    const line = document.querySelector(`tr[id="${id}"]`);
    if (originalRows[id]) {
        line.innerHTML = originalRows[id];
        htmx.process(line);
        const updateButton = line.querySelector(".edit-button");
        if (updateButton) {
            updateButton.addEventListener("click", async function (event) {
                await editLine(id);
            });
        }
    }
}

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

// Cria a configuração base do Toast
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end', // Fica no canto superior direito
    showConfirmButton: false, // Tira os botões
    timer: 3000, // Tempo que ele fica na tela (3 segundos)
    timerProgressBar: true, // Barrinha de tempo correndo no fundo
    
    // Pausa o tempo se o usuário passar o mouse em cima
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    },
    
    // Injeta as classes CSS customizadas para a animação
    showClass: {
        popup: 'swal-toast-anim-in'
    },
    hideClass: {
        popup: 'swal-toast-anim-out'
    },
    customClass: {
        title: 'swal-toast-title'
    }
});

// Escuta o evento que vem do FastAPI (ex: quando adiciona ou edita um item)
document.body.addEventListener('mostrarAlerta', function (e) {
    const dados = e.detail;
    
    // Dispara o Toast com os dados recebidos
    Toast.fire({
        icon: dados.icone || 'success',
        title: dados.mensagem || 'Ação realizada com sucesso!'
    });
});