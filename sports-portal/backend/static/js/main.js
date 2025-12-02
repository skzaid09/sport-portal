function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(() => {
        window.location.href = '/';
    })
    .catch(err => {
        console.error('Logout failed:', err);
        alert('Logout failed. Please try again.');
    });
}

function showToast(message, type = 'info') {
    const toastDiv = document.createElement('div');
    toastDiv.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toastDiv.setAttribute('role', 'alert');
    toastDiv.setAttribute('aria-live', 'assertive');
    toastDiv.setAttribute('aria-atomic', 'true');
    toastDiv.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    document.body.appendChild(toastDiv);
    const toast = new bootstrap.Toast(toastDiv, { delay: 3000 });
    toast.show();
    toastDiv.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toastDiv);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});