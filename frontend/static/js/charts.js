document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('graficoAnual').getContext('2d');
    
    // Configuramos gradientes
    const gradIngresos = ctx.createLinearGradient(0, 0, 0, 400);
    gradIngresos.addColorStop(0, '#2ecc71');
    gradIngresos.addColorStop(1, '#27ae60');

    const gradGastos = ctx.createLinearGradient(0, 0, 0, 400);
    gradGastos.addColorStop(0, '#ff7675');
    gradGastos.addColorStop(1, '#d63031');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datosAnuales.labels,
            datasets: [
                {
                    label: 'Ingresos',
                    data: datosAnuales.ingresos,
                    backgroundColor: gradIngresos,
                    borderRadius: 6,
                },
                {
                    label: 'Gastos',
                    data: datosAnuales.gastos,
                    backgroundColor: gradGastos,
                    borderRadius: 6,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: '#f0f0f0' },
                    ticks: { font: { size: 10 } }
                },
                x: { 
                    grid: { display: false },
                    ticks: { font: { size: 10 } }
                }
            }
        }
    });
});

// Gráfico de Categorías (Donut)
const ctxCat = document.getElementById('graficoCategorias').getContext('2d');

new Chart(ctxCat, {
    type: 'doughnut',
    data: {
        labels: labelsCat, // Estos datos los pasaremos desde el HTML
        datasets: [{
            data: valuesCat,
            backgroundColor: [
                '#3498db', '#9b59b6', '#f1c40f', '#e67e22', '#e74c3c', '#1abc9c'
            ],
            borderWidth: 2,
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { boxWidth: 12, font: { size: 11 } }
            }
        },
        cutout: '70%' // Hace que sea un anillo (donut) más fino y elegante
    }
});