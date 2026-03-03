async function loadData() {
    try {
        const response = await fetch("http://127.0.0.1:8000/get_all");
        const data = await response.json();
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = "";
        data.forEach(item => {
            const line = document.createElement("tr")
            const valueColor = item.type === 'receita' ? 'green' : 'red';
            const date_item = item.date_item.split('-').reverse().join('/'); 
            line.innerHTML = `
                <td>${item.category}</td>
                <td style="color: ${valueColor};">R$ ${item.value}</td>
                <td>${item.type}</td>
                <td>${date_item}</td>
            `;
            tableBody.appendChild(line);
        });
    } catch (error) {
        console.error("Erro ao carregar os dados:", error);
    }
}

loadData();

async function loadAmount() {
    try {
        const response = await fetch("http://127.0.0.1:8000/total-amount")
        const data = await response.json();
        const amountElement = document.getElementById("current-balance")
        amountElement.textContent = `Saldo Atual: R$ ${data["total-amount"].toFixed(2)}`;
    } catch (error) {
        console.error("Erro ao carregar o saldo:", error);
    }
}

loadAmount()

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
        const response = await fetch("http://127.0.0.1:8000/send-item", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newTransaction)
        })
        if (response.ok) {
            alert("Item adicionado com sucesso!");
            form.reset();
            loadData();
            loadAmount();
        } else {
            alert("Erro ao adicionar o item. Por favor, tente novamente.");
        }
        } catch (error) {
            console.error("Erro ao enviar o item:", error);
            alert("Erro ao enviar o item. Por favor, tente novamente.");
        }
});