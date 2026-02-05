document.addEventListener('DOMContentLoaded', () => {
    console.log("JS de Gastos cargado. Verificando datos...");

    // 1. MODAL (Abrir/Cerrar)
    const modal = document.getElementById('modalGasto');
    const btnOpen = document.getElementById('openModal');
    const btnClose = document.querySelector('.close-modal');

    if (btnOpen) btnOpen.onclick = () => { modal.style.display = 'flex'; };
    if (btnClose) btnClose.onclick = () => { modal.style.display = 'none'; };
    window.onclick = (e) => { if (e.target == modal) modal.style.display = 'none'; };

    // 2. FORMULARIO DINÁMICO (Categorías -> Subcategorías)
    const catRadios = document.querySelectorAll('input[name="categoria"]');
    const subcatWrapper = document.getElementById('subcat-wrapper');
    const selectSubcat = document.getElementById('select-subcat');

    catRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const catId = this.dataset.id;
            if(subcatWrapper) subcatWrapper.style.display = 'block';
            if(selectSubcat) {
                selectSubcat.innerHTML = '<option>Cargando...</option>';
                fetch(`/api/subcategorias/${catId}`)
                    .then(res => res.json())
                    .then(data => {
                        selectSubcat.innerHTML = '';
                        data.forEach(sub => {
                            const opt = document.createElement('option');
                            opt.value = sub.nombre;
                            opt.textContent = sub.nombre;
                            selectSubcat.appendChild(opt);
                        });
                    });
            }
        });
    });

    // --- RENDERIZADO DE GRÁFICOS ---

    // 3. Gráfico Evolución Semanal (Líneas)
    const ctxSem = document.getElementById('chartSemanas');
    if (ctxSem && typeof dataSem !== 'undefined' && dataSem.length > 0) {
        new Chart(ctxSem, {
            type: 'line',
            data: {
                labels: ['S1', 'S2', 'S3', 'S4', 'S5'],
                datasets: [{
                    data: dataSem,
                    borderColor: '#752343',
                    backgroundColor: 'rgba(117, 35, 67, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            // Esto añade el € al pasar el ratón sobre las barras
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) label += ': ';
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
                        beginAtZero: true,
                        // 1. LÍNEAS DE FONDO (como en ingresos)
                        grid: {
                            color: 'rgba(117, 35, 67, 0.1)', // Burdeos muy clarito
                            drawBorder: false
                        },
                        ticks: {
                            color: '#bbb',
                            font: { size: 10 },
                            // 2. AÑADIR € AL EJE Y
                            callback: function(value) {
                                return value + '€';
                            }
                        }
                    },
                    x: {
                        grid: { display: false }, // Sin líneas verticales para que sea limpio
                        ticks: { color: '#bbb', font: { size: 10 } }
                    }
                }
            }
        });
    }

    // 4. Gráfico Reparto por Categoría (Dona)
    // --- DENTRO DE GASTOS.JS ---

    const ctxCat = document.getElementById('chartCategorias').getContext('2d');

    new Chart(ctxCat, {
        type: 'doughnut',
        data: {
            labels: labelsCat,
            datasets: [{
                data: valuesCat,
                backgroundColor: ['#752343', '#9b3054', '#c24d6f', '#e07693', '#f2a7ba', '#444'],
                borderWidth: 3,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%', // Lo hace un poco más fino y elegante
            plugins: {
                // 1. ACTIVAR LEYENDA
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#752343', // Color burdeos para los textos
                        font: { weight: 'bold', size: 12 },
                        padding: 20
                    }
                },
                // 2. FORMATO MONEDA Y PORCENTAJE AL PASAR EL CURSOR
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const dataset = context.dataset.data;
                            const total = dataset.reduce((acc, curr) => acc + curr, 0);
                            const valorActual = context.raw;
                            const porcentaje = ((valorActual / total) * 100).toFixed(1);
                            
                            // Formato 0,00 €
                            const formatoDinero = new Intl.NumberFormat('es-ES', { 
                                style: 'currency', 
                                currency: 'EUR' 
                            }).format(valorActual);
                            
                            return ` ${context.label}: ${formatoDinero} (${porcentaje}%)`;
                        }
                    }
                }
            }
        }
    });

    // 5. Gráficos Mini de Subcategorías (Los que no salían)
    if (typeof statsSub !== 'undefined' && statsSub !== null) {
        Object.entries(statsSub).forEach(([catNombre, data], index) => {
            const canvasId = `chart_sub_${index + 1}`; 
            const ctxSub = document.getElementById(canvasId);
            
            if (ctxSub) {
                const subLabels = Object.keys(data.subcategorias);
                const subValues = Object.values(data.subcategorias);

                new Chart(ctxSub, {
                    type: 'bar',
                    data: {
                        labels: subLabels,
                        datasets: [{
                            data: subValues,
                            backgroundColor: '#752343',
                            borderRadius: 6
                        }]
                    },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false },
                        // AÑADIMOS EL TOOLTIP AQUÍ
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const dataset = context.dataset.data;
                                    // Sumamos el total de esa categoría para sacar el %
                                    const total = dataset.reduce((acc, curr) => acc + curr, 0);
                                    const valorActual = context.raw;
                                    const porcentaje = ((valorActual / total) * 100).toFixed(1);
                                    
                                    // Formato 0,00 €
                                    const formatoDinero = new Intl.NumberFormat('es-ES', { 
                                        style: 'currency', 
                                        currency: 'EUR' 
                                    }).format(valorActual);
                                    
                                    return ` ${context.label}: ${formatoDinero} (${porcentaje}%)`;
                                }
                            }
                        }
                    },
    scales: { 
        x: { display: false }, 
        y: { 
            ticks: { 
                font: { weight: 'bold', size: 11 },
                color: '#752343' // Nombres de subcategorías en burdeos
            }, 
            grid: { display: false } 
        } 
    }
}
                });
            }
        });
    }
});

// FUNCIONES GLOBALES (Borrado)
function eliminarGasto(id) {
    if (confirm('¿Seguro que quieres borrar este gasto?')) {
        fetch(`/eliminar_gasto/${id}`, { method: 'DELETE' })
        .then(res => res.ok ? location.reload() : alert("Error al borrar"));
    }
}

function toggleAdmin() {
    const panel = document.getElementById('admin-panel');
    if(panel) panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function eliminarCatPrincipal(id) { if(confirm("¿Borrar categoría y todas sus subcategorías?")) ejecutarBorrado('/gastos/eliminar_categoria/' + id); }
function eliminarSubcategoria(id) { if(confirm("¿Borrar esta subcategoría?")) ejecutarBorrado('/gastos/eliminar_subcategoria/' + id); }
function ejecutarBorrado(url) {
    fetch(url, { method: 'DELETE' }).then(res => res.ok ? location.reload() : alert("Error al borrar"));
}