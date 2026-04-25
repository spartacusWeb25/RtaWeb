(function () {
    const html = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const icon = document.getElementById('themeIcon');

    function applyTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);

        if (!themeToggle || !icon) {
            return;
        }

        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill';
            themeToggle.classList.remove('btn-outline-dark');
            themeToggle.classList.add('btn-outline-light');
        } else {
            icon.className = 'bi bi-moon-fill';
            themeToggle.classList.remove('btn-outline-light');
            themeToggle.classList.add('btn-outline-dark');
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        applyTheme(localStorage.getItem('theme') || 'dark');

        themeToggle?.addEventListener('click', () => {
            const current = html.getAttribute('data-bs-theme');
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });

        document.querySelectorAll('[data-clear-target]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const input = document.getElementById(btn.dataset.clearTarget);
                if (input) {
                    input.value = '';
                    input.focus();
                }
            });
        });

        const senhaInput = document.getElementById('id_senha');
        const toggleSenhaBtn = document.getElementById('toggleSenha');

        toggleSenhaBtn?.addEventListener('click', () => {
            if (!senhaInput) {
                return;
            }
            const mostrando = senhaInput.type === 'text';
            senhaInput.type = mostrando ? 'password' : 'text';
            toggleSenhaBtn.innerHTML = mostrando
                ? '<i class="bi bi-eye"></i>'
                : '<i class="bi bi-eye-slash"></i>';
        });

        const loginForm = document.getElementById('loginForm');
        const submitBtn = document.getElementById('submitBtn');
        const submitLabel = submitBtn?.querySelector('.btn-label');
        const submitSpinner = submitBtn?.querySelector('.spinner-border');
        const progressWrapper = document.getElementById('loginProgressWrapper');
        const progressBar = document.getElementById('loginProgressBar');

        if (!loginForm || !submitBtn || !submitLabel || !submitSpinner || !progressWrapper || !progressBar) {
            return;
        }

        let progressTimer = null;

        loginForm.addEventListener('submit', () => {
            submitBtn.disabled = true;
            submitLabel.textContent = 'Entrando...';
            submitSpinner.classList.remove('d-none');
            progressWrapper.classList.add('show');

            let progress = 18;
            progressBar.style.width = `${progress}%`;

            progressTimer = setInterval(() => {
                if (progress >= 94) {
                    clearInterval(progressTimer);
                    return;
                }
                progress += Math.floor(Math.random() * 9) + 2;
                if (progress > 94) progress = 94;
                progressBar.style.width = `${progress}%`;
            }, 180);
        });

        window.addEventListener('pageshow', () => {
            clearInterval(progressTimer);
        });
    });
})();
