document.addEventListener('DOMContentLoaded', () => {
    // Modal
    const modal = document.getElementById('modalIngreso');
    const btnOpen = document.getElementById('openModal');
    const btnClose = document.querySelector('.close-modal');

    if (btnOpen) btnOpen.onclick = () => modal.style.display = 'flex';
    if (btnClose) btnClose.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => { if (e.target == modal) modal.style.display = 'none'; };

    // Gráfico Semanal con €
    const ctxSem = document.getElementById('chartSemanas');
    if (ctxSem) {
        new Chart(ctxSem, {
            type: 'line',
            data: {
                labels: ['S1', 'S2', 'S3', 'S4', 'S5'],
                datasets: [{
                    data: dataSem,
                    borderColor: '#752343',
                    backgroundColor: 'rgba(117, 35, 67, 0.05)',
                    fill: true, tension: 0.4
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { 
                    legend: { display: false },
                    tooltip: { callbacks: { label: (ctx) => ` ${ctx.raw}€` } }
                },
                scales: {
                    y: { ticks: { callback: (v) => v + '€' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // Anillo con %
    const ctxDon = document.getElementById('chartCategorias');
    if (ctxDon) {
        new Chart(ctxDon, {
            type: 'doughnut',
            data: {
                labels: labelsCat,
                datasets: [{
                    data: valuesCat,
                    backgroundColor: ['#752343', '#a33b5d', '#d67d99', '#ffccd5'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right' },
                    tooltip: {
                        callbacks: {
                            label: (item) => {
                                let total = item.dataset.data.reduce((a, b) => a + b, 0);
                                let perc = ((item.raw / total) * 100).toFixed(1) + '%';
                                return ` ${item.label}: ${item.raw}€ (${perc})`;
                            }
                        }
                    }
                }
            }
        });
    }
});

function cambiarMes(mes) { window.location.href = "/ingresos?mes=" + mes; }

function eliminarIngreso(id) {
    if (confirm('¿Deseas eliminar este registro?')) {
        // La URL ahora es /ingresos/eliminar_ingreso/... 
        // o simplemente /eliminar_ingreso/ si el blueprint no tiene prefix
        fetch(`/eliminar_ingreso/${id}`, { 
            method: 'DELETE' 
        }).then(res => {
            if (res.ok) window.location.reload();
        });
    }
}