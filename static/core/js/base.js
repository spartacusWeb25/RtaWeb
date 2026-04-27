(function () {
    const html = document.documentElement;

    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('rtaweb-theme', theme);
        const icon = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        document.querySelectorAll('.js-theme-icon').forEach((el) => {
            el.className = icon;
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        applyTheme(localStorage.getItem('rtaweb-theme') || 'light');

        document.querySelectorAll('.js-theme-btn').forEach((btn) => {
            btn.addEventListener('click', () => {
                applyTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
            });
        });

        const navToggle = document.getElementById('navToggle');
        const navMobilePanel = document.getElementById('navMobilePanel');
        if (navToggle && navMobilePanel) {
            navToggle.addEventListener('click', () => {
                navMobilePanel.classList.toggle('open');
            });

            navMobilePanel.querySelectorAll('.nav-item > .nav-btn').forEach((button) => {
                button.addEventListener('click', () => {
                    if (window.innerWidth > 768) {
                        return;
                    }

                    const item = button.parentElement;
                    const shouldOpen = !item.classList.contains('is-open');

                    navMobilePanel.querySelectorAll('.nav-item.is-open').forEach((openItem) => {
                        openItem.classList.remove('is-open');
                    });

                    if (shouldOpen) {
                        item.classList.add('is-open');
                    }
                });
            });
        }

        document.querySelectorAll('.sortable-submenu').forEach((menu) => {
            [...menu.children]
                .sort((a, b) => a.textContent.trim().localeCompare(b.textContent.trim(), 'pt-BR'))
                .forEach((el) => menu.appendChild(el));
        });
    });
})();
