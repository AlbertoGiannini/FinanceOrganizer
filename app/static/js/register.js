// API_URL = "https://myfinancesaver.vercel.app/auth"
const API_URL = "http://127.0.0.1:8000/auth";

const form = document.querySelector('form');
document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    if (data.password != data.confirm_password) {
        alert("As senhas não coincidem.");
        form.reset();
        return;
    } 

    const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    if (response.ok) {
        alert('Cadastro realizado com sucesso! Um email de confirmação foi enviado para o seu e-mail.')
        window.location.href = "/login";
    } else {
        const responseError = await response.json();
        alert(`Erro ao fazer login. Por favor, tente novamente. - ${responseError.detail}`);
    }
});
