(function () {
    function getExitUrl() {
        const exitLink = document.querySelector('.js-esc-exit[href]');
        if (!exitLink) {
            return '';
        }
        return exitLink.getAttribute('href') || '';
    }

    function isVisible(element) {
        return !!(element && element.offsetParent !== null);
    }

    function closeVisibleAlert() {
        const alerts = Array.from(document.querySelectorAll('.page-content .alert:not(.toast)'));
        const visibleAlert = alerts.find(isVisible);

        if (!visibleAlert) {
            return false;
        }

        if (window.bootstrap && window.bootstrap.Alert) {
            window.bootstrap.Alert.getOrCreateInstance(visibleAlert).close();
        } else {
            visibleAlert.remove();
        }

        return true;
    }

    document.addEventListener('keydown', function (event) {
        if (event.key !== 'Escape') {
            return;
        }

        // Preserve Esc for open Bootstrap modals.
        if (document.querySelector('.modal.show')) {
            return;
        }

        if (closeVisibleAlert()) {
            return;
        }

        const exitUrl = getExitUrl();
        if (!exitUrl) {
            return;
        }

        window.location.href = exitUrl;
    });
})();
