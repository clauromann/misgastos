document.addEventListener('DOMContentLoaded', () => {
    // 1. GRÁFICO DE LÍNEAS (EVOLUCIÓN)
    const ctxLineas = document.getElementById('chartEvolucionAnual').getContext('2d');
    
    const gradAhorro = ctxLineas.createLinearGradient(0, 0, 0, 400);
    gradAhorro.addColorStop(0, 'rgba(117, 35, 67, 0.25)');
    gradAhorro.addColorStop(1, 'rgba(117, 35, 67, 0)');

    new Chart(ctxLineas, {
        type: 'line',
        data: {
            labels: mesesLabels,
            datasets: [
                { 
                    label: 'Ingresos', 
                    data: lineasData.ingresos, 
                    borderColor: '#2ecc71', 
                    borderWidth: 2, 
                    tension: 0.4, 
                    pointRadius: 4,
                    pointBackgroundColor: '#2ecc71' 
                },
                { 
                    label: 'Gastos', 
                    data: lineasData.gastos, 
                    borderColor: '#e74c3c', 
                    borderWidth: 2, 
                    tension: 0.4, 
                    pointRadius: 4,
                    pointBackgroundColor: '#e74c3c'
                },
                { 
                    label: 'Ahorro', 
                    data: lineasData.ahorros, 
                    borderColor: '#752343', 
                    backgroundColor: gradAhorro, 
                    fill: true, 
                    borderWidth: 4, 
                    tension: 0.4, 
                    pointRadius: 4,
                    pointBackgroundColor: '#752343'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: { color: '#752343', font: { weight: 'bold', size: 11 }, padding: 20 }
                },
                // FORMATEO DEL CURSOR (HOVER)
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) { label += ': '; }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: { 
                    grid: { color: 'rgba(117, 35, 67, 0.05)' },
                    ticks: { 
                        color: '#bbb', 
                        font: { size: 10 },
                        callback: function(value) { return value + '€'; }
                    }
                },
                x: { 
                    grid: { display: false },
                    ticks: { color: '#bbb', font: { size: 10 } }
                }
            }
        }
    });

    // 2. GRÁFICO DE TORTA (DISTRIBUCIÓN CON PORCENTAJES)
    const ctxPie = document.getElementById('chartGastosAnual').getContext('2d');
    new Chart(ctxPie, {
        type: 'doughnut',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieValues,
                backgroundColor: ['#752343', '#9b3054', '#c24d6f', '#e07693', '#f2a7ba', '#444'],
                borderWidth: 3,
                borderColor: '#fdf2f2'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#752343', font: { weight: 'bold', size: 11 } }
                },
                // FORMATEO DEL CURSOR: CANTIDAD + PORCENTAJE
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const dataset = context.dataset.data;
                            const total = dataset.reduce((acc, curr) => acc + curr, 0);
                            const valorActual = context.raw;
                            const porcentaje = ((valorActual / total) * 100).toFixed(1);
                            const formatoDinero = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(valorActual);
                            
                            return ` ${context.label}: ${formatoDinero} (${porcentaje}%)`;
                        }
                    }
                }
            }
        }
    });
});