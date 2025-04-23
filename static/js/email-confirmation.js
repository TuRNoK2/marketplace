// Обработка подтверждения email
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для кнопки повторной отправки
    const resendBtn = document.getElementById('resend-confirmation');
    if (resendBtn) {
        resendBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');

            // Блокируем кнопку на время отправки
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Отправка...';

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(new FormData(form))
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('Письмо с подтверждением отправлено!');
                } else {
                    showToast(data.error || 'Ошибка при отправке письма', 'danger');
                }
            })
            .catch(error => {
                showToast('Ошибка сети', 'danger');
            })
            .finally(() => {
                this.disabled = false;
                this.innerHTML = '<i class="bi bi-envelope-plus me-1"></i> Отправить письмо повторно';
            });
        });
    }
});

// Функция для показа toast-уведомлений
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;

    const toastEl = document.createElement('div');
    toastEl.className = `toast show align-items-center text-white bg-${type}`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);

    setTimeout(() => {
        toastEl.remove();
    }, 5000);
}