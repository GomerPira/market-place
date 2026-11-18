/**
 * Fountain Engine Marketplace — frontend cliente.
 * Servicio mínimo: añadir al carrito y actualizar el contador.
 */
(function () {
  'use strict';

  const cartCountEl = document.getElementById('cart-count');
  if (cartCountEl) {
    fetch('/api/cart')
      .then((res) => res.json())
      .then((data) => {
        cartCountEl.textContent = Array.isArray(data) ? data.length : Object.keys(data).length;
      })
      .catch(() => {
        cartCountEl.textContent = 0;
      });
  }

  document.addEventListener('click', (event) => {
    const button = event.target.closest('.add-to-cart');
    if (!button) return;

    event.preventDefault();
    const resourceId = button.dataset.id;

    fetch('/api/cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resource_id: resourceId, quantity: 1 })
    })
      .then((res) => res.json())
      .then((data) => {
        const count = Array.isArray(data) ? data.length : Object.keys(data).length;
        if (cartCountEl) {
          cartCountEl.textContent = count;
        }
        alert('Producto añadido al carrito.');
        if (data.cart && data.cart[resourceId]) {
          alert('Cantidad actual: ' + data.cart[resourceId]);
        }
      })
      .catch(() => {
        alert('No se pudo comunicar con el servidor.');
      });
  });
})();
