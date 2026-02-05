document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', (e) => {
            const username = document.getElementById('username').value;
            if (username.length < 4) {
                alert('El nombre de usuario debe tener al menos 4 caracteres');
                e.preventDefault();
            }
        });
    }
});