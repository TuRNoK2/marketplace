// cart.js - модуль корзины
class Cart {
  constructor() {
    this.cartKey = 'ecommerce_cart';
    this.init();
  }

  init() {
    // Инициализация корзины при загрузке
    if (!this.getCart()) {
      this.saveCart([]);
    }
    this.updateCartCounter();
  }

  getCart() {
    return JSON.parse(localStorage.getItem(this.cartKey)) || [];
  }

  saveCart(cart) {
    localStorage.setItem(this.cartKey, JSON.stringify(cart));
    this.updateCartCounter();
    return cart;
  }

  addItem(product) {
    const cart = this.getCart();
    const existingItem = cart.find(item => item.id === product.id);

    if (existingItem) {
      existingItem.quantity += product.quantity || 1;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image || '',
        quantity: product.quantity || 1
      });
    }

    this.saveCart(cart);
    this.showToast(`${product.name} добавлен в корзину!`);
    return cart;
  }

  removeItem(productId) {
    const cart = this.getCart().filter(item => item.id !== productId);
    this.saveCart(cart);
    this.showToast('Товар удален из корзины');
    return cart;
  }

  updateQuantity(productId, quantity) {
    const cart = this.getCart();
    const item = cart.find(item => item.id === productId);

    if (item) {
      if (quantity > 0) {
        item.quantity = quantity;
      } else {
        return this.removeItem(productId);
      }
    }

    return this.saveCart(cart);
  }

  getTotalItems() {
    return this.getCart().reduce((total, item) => total + item.quantity, 0);
  }

  getTotalPrice() {
    return this.getCart().reduce((total, item) => total + (item.price * item.quantity), 0);
  }

  clearCart() {
    this.saveCart([]);
    return [];
  }

  updateCartCounter() {
    const totalItems = this.getTotalItems();
    document.querySelectorAll('.cart-counter').forEach(el => {
      el.textContent = totalItems;
      el.style.display = totalItems > 0 ? 'block' : 'none';
    });
  }

  showToast(message) {
    // Создаем toast если его нет
    let toastEl = document.getElementById('cart-toast');
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.id = 'cart-toast';
      toastEl.className = 'toast align-items-center text-white bg-success';
      toastEl.style.position = 'fixed';
      toastEl.style.bottom = '20px';
      toastEl.style.right = '20px';
      toastEl.style.zIndex = '1100';

      toastEl.innerHTML = `
        <div class="d-flex">
          <div class="toast-body">${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      `;

      document.body.appendChild(toastEl);
    } else {
      toastEl.querySelector('.toast-body').textContent = message;
    }

    // Показываем toast
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }

  renderCart() {
    const cart = this.getCart();
    const container = document.getElementById('cart-items-container');
    const totalElement = document.getElementById('cart-total-price');
    const emptyElement = document.getElementById('empty-cart-message');

    if (!container) return;

    if (cart.length === 0) {
      if (emptyElement) emptyElement.style.display = 'block';
      if (totalElement) totalElement.textContent = '0';
      container.innerHTML = '';
      return;
    }

    if (emptyElement) emptyElement.style.display = 'none';

    let html = '';
    cart.forEach(item => {
      const itemTotal = item.price * item.quantity;

      html += `
        <div class="card mb-3">
          <div class="row g-0">
            <div class="col-md-2">
              <img src="${item.image || '/static/img/no-image.png'}" class="img-fluid rounded-start" alt="${item.name}">
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">${item.name}</h5>
                <p class="card-text">${item.price} $ × ${item.quantity} = ${itemTotal.toFixed(2)} $</p>
                <div class="input-group" style="width: 150px;">
                  <button class="btn btn-outline-secondary" onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                  <input type="number" class="form-control text-center" value="${item.quantity}"
                         onchange="cart.updateQuantity('${item.id}', this.value)">
                  <button class="btn btn-outline-secondary" onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
                </div>
              </div>
            </div>
            <div class="col-md-2 d-flex align-items-center justify-content-end">
              <button class="btn btn-danger" onclick="cart.removeItem('${item.id}')">
                <i class="bi bi-trash"></i> Удалить
              </button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
    if (totalElement) totalElement.textContent = this.getTotalPrice().toFixed(2);
  }
}

// Создаем экземпляр корзины
const cart = new Cart();

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  cart.updateCartCounter();

  // Если на странице есть контейнер корзины - рендерим товары
  if (document.getElementById('cart-items-container')) {
    cart.renderCart();
  }
});

// Делаем cart доступной в глобальной области видимости
window.cart = cart;