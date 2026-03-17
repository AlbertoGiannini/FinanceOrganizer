//API_URL = "https://myfinancesaver.vercel.app/auth"
API_URL = "http://127.0.0.1:8000/auth";
const form = document.querySelector('form');
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    if (response.ok) {
        window.location.href = "/";
    } else {
        const responseError = await response.json();
        alert(`Erro ao fazer login. Por favor, tente novamente. - ${responseError.detail}`);
    }
});
