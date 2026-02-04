function eliminarHucha(id) {
    if (confirm('¿Quieres eliminar esta hucha y todos sus movimientos?')) {
        fetch(`/eliminar_hucha/${id}`, { method: 'DELETE' })
        .then(res => {
            if (res.ok) window.location.reload();
        });
    }
}

function eliminarAhorro(id) {
    if (confirm('¿Eliminar registro de ahorro?')) {
        fetch(`/eliminar_ahorro/${id}`, { method: 'DELETE' })
        .then(res => {
            if (res.ok) window.location.reload();
        });
    }
}