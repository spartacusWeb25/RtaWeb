(function () {
    function getToastIcon(toastEl) {
        if (toastEl.classList.contains('rta-toast-success')) return 'bi-check-circle-fill';
        if (toastEl.classList.contains('rta-toast-error') || toastEl.classList.contains('rta-toast-danger')) return 'bi-exclamation-octagon-fill';
        if (toastEl.classList.contains('rta-toast-warning')) return 'bi-exclamation-triangle-fill';
        return 'bi-info-circle-fill';
    }

    function bootToasts() {
        if (!window.bootstrap) return;
        document.querySelectorAll('.rta-toast').forEach((toastEl) => {
            const iconEl = toastEl.querySelector('.toast-icon');
            if (iconEl) {
                iconEl.className = `bi toast-icon ${getToastIcon(toastEl)}`;
            }

            if (toastEl.dataset.autoshow === 'true') {
                const toast = bootstrap.Toast.getOrCreateInstance(toastEl);
                toast.show();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', bootToasts);
})();
