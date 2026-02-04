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
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, grid: { color: '#f5f5f5' } }, x: { grid: { display: false } } }
            }
        });
    }

    // 4. Gráfico Reparto por Categoría (Dona)
    const ctxCat = document.getElementById('chartCategorias');
    if (ctxCat && typeof labelsCat !== 'undefined' && labelsCat.length > 0) {
        new Chart(ctxCat, {
            type: 'doughnut',
            data: {
                labels: labelsCat,
                datasets: [{
                    data: valuesCat,
                    backgroundColor: ['#752343', '#9b3054', '#c24d6f', '#e07693', '#f2a7ba', '#444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } },
                cutout: '70%'
            }
        });
    }

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
                        indexAxis: 'y', // Barra horizontal para mejor lectura
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { 
                            x: { display: false }, 
                            y: { ticks: { font: { weight: 'bold', size: 10 } }, grid: { display: false } } 
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