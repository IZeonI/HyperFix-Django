function cambiarCantidad(cambio) {
    const input = document.getElementById("cantidad");
    const contenedor = input.closest(".cantidad-control");
    const stock = parseInt(contenedor.dataset.stock);
    const btnSumar = document.getElementById("btn-sumar");
    const btnRestar = document.getElementById("btn-restar");

    let valor = parseInt(input.value) || 1;
    valor = Math.max(1, Math.min(stock, valor + cambio));
    input.value = valor;

    btnRestar.disabled = valor <= 1;
    btnSumar.disabled = valor >= stock;
}

function actualizarCantidadHidden() {
    const cantidad = document.getElementById("cantidad").value;
    document.getElementById("cantidad-hidden").value = cantidad;
    return true; 
}

document.addEventListener("DOMContentLoaded", () => cambiarCantidad(0));