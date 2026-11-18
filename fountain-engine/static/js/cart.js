(function () {
  'use strict';

  const updateCount = () => {
    fetch('/api/cart')
      .then((res) => res.json())
      .then((data) => {
        const count = Array.isArray(data) ? data.length : Object.keys(data).length;
        document.getElementById('cart-count').textContent = count;
      })
      .catch(() => {});
  };

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
        document.getElementById('cart-count').textContent = count;
      })
      .catch(() => {});
  });

  setInterval(updateCount, 60000);
  updateCount();
})();
