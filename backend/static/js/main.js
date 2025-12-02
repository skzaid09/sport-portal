// backend/static/js/main.js

// Unified logout function — works for all roles
function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(() => {
        // Redirect to home after logout
        window.location.href = '/';
    })
    .catch(err => {
        console.error('Logout failed:', err);
        alert('Logout failed. Please try again.');
    });
}

// Show toast-like alert (optional enhancement)
function showToast(message, type = 'info') {
    // Create toast dynamically
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

    // Add to body
    document.body.appendChild(toastDiv);

    // Initialize Bootstrap Toast
    const toast = new bootstrap.Toast(toastDiv, { delay: 3000 });
    toast.show();

    // Remove after hide
    toastDiv.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toastDiv);
    });
}

// Auto-initialize Bootstrap tooltips (if used)
document.addEventListener('DOMContentLoaded', () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});