document.addEventListener('DOMContentLoaded', function() {
    const cantidadInput = document.getElementById('cantidadInput');
    
    // Al abrir la página, que el foco vaya directo al número
    // (Muy cómodo en iPhone para que salga el teclado numérico rápido)
    setTimeout(() => {
        cantidadInput.focus();
    }, 500);

    // Animación simple al enviar
    const form = document.getElementById('formIngreso');
    form.addEventListener('submit', function() {
        const btn = document.querySelector('.submit-btn-ingreso');
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
        btn.style.opacity = '0.7';
    });
});