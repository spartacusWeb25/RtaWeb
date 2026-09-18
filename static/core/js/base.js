function sortMainMenus() {
  ;['navMenusDesktop', 'navMenusMobile'].forEach((id) => {
    const menu = document.getElementById(id)
    if (!menu) return
    ;[...menu.children]
      .sort((a, b) =>
        a.textContent.trim().localeCompare(b.textContent.trim(), 'pt-BR', {
          sensitivity: 'base',
        }),
      )
      .forEach((el) => menu.appendChild(el))
  })
}

function initInfiniteScroll() {
  document.querySelectorAll('[data-infinite-scroll-root]').forEach((root) => {
    const itemsSelector =
      root.getAttribute('data-infinite-scroll-items-selector') ||
      '[data-infinite-scroll-items]'

    const sentinel = root.querySelector('[data-infinite-scroll-sentinel]')
    const status = root.querySelector('[data-infinite-scroll-status]')
    const items = document.querySelector(itemsSelector)

    if (!sentinel || !items) return

    let nextUrl = root.getAttribute('data-infinite-scroll-next-url') || ''
    let isLoading = false

    async function loadNext() {
      if (isLoading || !nextUrl) return
      isLoading = true

      root.classList.add('is-loading')
      if (status) status.textContent = 'Carregando...'

      try {
        const res = await fetch(nextUrl, {
          headers: { 'X-Infinite-Scroll': '1' },
        })

        if (!res.ok) {
          nextUrl = ''
          return
        }

        const html = await res.text()
        const doc = new DOMParser().parseFromString(html, 'text/html')
        const incomingItems = doc.querySelector(itemsSelector)

        if (!incomingItems) {
          nextUrl = ''
          return
        }

        items.insertAdjacentHTML('beforeend', incomingItems.innerHTML)

        const incomingRoot = doc.querySelector('[data-infinite-scroll-root]')
        nextUrl =
          incomingRoot?.getAttribute('data-infinite-scroll-next-url') || ''
        root.setAttribute('data-infinite-scroll-next-url', nextUrl)
      } catch (e) {
        nextUrl = ''
      } finally {
        isLoading = false
        root.classList.remove('is-loading')

        if (!nextUrl) {
          observer.disconnect()
          root.remove()
        }
      }
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          loadNext()
        }
      },
      { rootMargin: '240px 0px' },
    )

    if (!nextUrl) {
      root.remove()
      return
    }

    observer.observe(sentinel)
  })
}

function initResponsiveFilterCollapse() {
  document.querySelectorAll('.filtros-collapse').forEach((collapse) => {
    const shouldOpen = window.innerWidth >= 769
    collapse.classList.toggle('show', shouldOpen)

    const button = document.querySelector(
      `[data-bs-target="#${collapse.id}"],[aria-controls="${collapse.id}"]`,
    )

    if (button) {
      button.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false')
    }
  })
}

function initNavSubmenuToggle() {
  try {
    const toggles = document.querySelectorAll('[data-submenu-toggle]')
    if (!toggles.length) return

    function getPanel(el) {
      return el && el.querySelector
        ? el.querySelector(':scope > .submenu-panel') || el.querySelector('.submenu-panel')
        : null
    }

    function closeAllSubmenus(exceptEl) {
      toggles.forEach((el) => {
        if (el !== exceptEl) {
          el.classList.remove('is-open')
          el.setAttribute('aria-expanded', 'false')
          const p = getPanel(el)
          if (p) p.style.display = 'none'
        }
      })
    }

    toggles.forEach((el) => {
      const handler = (e) => {
        if (e) {
          const targetLink = e.target.closest && e.target.closest('a[href]')
          if (targetLink) {
            return
          }
          const insidePanel = e.target.closest && e.target.closest('.submenu-panel')
          if (insidePanel) {
            return
          }
          e.preventDefault && e.preventDefault()
          e.stopPropagation && e.stopPropagation()
        }
        const isOpen = el.classList.contains('is-open')
        const panel = getPanel(el)
        closeAllSubmenus(el)
        if (isOpen) {
          el.classList.remove('is-open')
          el.setAttribute('aria-expanded', 'false')
          if (panel) panel.style.display = 'none'
        } else {
          el.classList.add('is-open')
          el.setAttribute('aria-expanded', 'true')
          if (panel) panel.style.display = 'block'
        }
      }
      el.addEventListener('click', handler)
      el.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          handler(e)
        } else if (e.key === 'Escape') {
          e.preventDefault()
          el.classList.remove('is-open')
          el.setAttribute('aria-expanded', 'false')
          const p = getPanel(el)
          if (p) p.style.display = 'none'
        }
      })
    })

    document.addEventListener(
      'click',
      (e) => {
        const inside =
          e.target.closest &&
          (e.target.closest('[data-submenu-toggle]') ||
            e.target.closest('.submenu-panel'))
        if (!inside) {
          closeAllSubmenus(null)
        }
      },
      true,
    )
  } catch (e) {
    try { if (window.console && console.warn) console.warn('[nav-submenu]', e) } catch (_e) {}
  }
}

function initRtaMessages() {
  try {
    const alerts = document.querySelectorAll('.rta-alert[data-rta-message="1"]')
    if (alerts.length === 0) return

    function hideAlertEl(alertEl) {
      if (!alertEl) return
      try {
        const bsAlert =
          typeof bootstrap !== 'undefined' && bootstrap && bootstrap.Alert
            ? bootstrap.Alert.getOrCreateInstance(alertEl)
            : null
        if (bsAlert && typeof bsAlert.close === 'function') {
          bsAlert.close()
        }
      } catch (e) { /* noop */ }
      try {
        // Garantia 100% — esconde visualmente mesmo que o close() falhe
        alertEl.style.setProperty('opacity', '0', 'important')
        alertEl.style.setProperty('height', '0px', 'important')
        alertEl.style.setProperty('min-height', '0px', 'important')
        alertEl.style.setProperty('padding-top', '0px', 'important')
        alertEl.style.setProperty('padding-bottom', '0px', 'important')
        alertEl.style.setProperty('margin-top', '0px', 'important')
        alertEl.style.setProperty('margin-bottom', '0px', 'important')
        alertEl.style.setProperty('border-width', '0px', 'important')
        alertEl.style.setProperty('pointer-events', 'none', 'important')
        alertEl.style.setProperty('visibility', 'hidden', 'important')
      } catch (e) { /* noop */ }
      try {
        // Remover do DOM após 300ms (transition)
        setTimeout(() => {
          if (alertEl && alertEl.parentNode) {
            alertEl.parentNode.removeChild(alertEl)
          }
        }, 350)
      } catch (e) { /* noop */ }
    }

    alerts.forEach((alertEl) => {
      const timeout = parseInt(alertEl.getAttribute('data-rta-timeout') || '5000', 10)
      if (timeout > 0) {
        setTimeout(() => hideAlertEl(alertEl), timeout)
      }
    })

    function dismissAllRtaMessages() {
      try {
        document.querySelectorAll('.rta-alert[data-rta-message="1"]').forEach((alertEl) => {
          hideAlertEl(alertEl)
        })
      } catch (e) { /* noop */ }
    }

    try {
      document.addEventListener(
        'click',
        (e) => {
          const link = e.target.closest && e.target.closest('a[href]')
          if (!link) return
          const href = (link.getAttribute('href') || '').toString()
          if (!href) return
          if (href === '#' || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) {
            return
          }
          const target = (link.getAttribute('target') || '').toString()
          if (target === '_blank') return
          dismissAllRtaMessages()
        },
        true,
      )
    } catch (e) { /* noop */ }

    try {
      window.addEventListener('beforeunload', dismissAllRtaMessages)
    } catch (e) { /* noop */ }
  } catch (e) {
    // NÃO deixa erro no initRtaMessages quebrar o resto do app
    try { if (window.console && console.warn) console.warn('[rta-messages]', e) } catch (_e) {}
  }
}

;(function () {
  const html = document.documentElement

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme)
    localStorage.setItem('rtaweb-theme', theme)
    const icon = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill'
    document.querySelectorAll('.js-theme-icon').forEach((el) => {
      el.className = icon
    })
  }

  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(localStorage.getItem('rtaweb-theme') || 'light')

    document.querySelectorAll('.js-theme-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        applyTheme(
          html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark',
        )
      })
    })
    initRtaMessages()
    initInfiniteScroll()
    initResponsiveFilterCollapse()
    initNavSubmenuToggle()
    const navToggle = document.getElementById('navToggle')
    const navMobilePanel = document.getElementById('navMobilePanel')
    if (navToggle && navMobilePanel) {
      navToggle.addEventListener('click', () => {
        navMobilePanel.classList.toggle('open')
      })

      navMobilePanel
        .querySelectorAll('.nav-item > .nav-btn')
        .forEach((button) => {
          button.addEventListener('click', () => {
            if (window.innerWidth > 768) {
              return
            }

            const item = button.parentElement
            const shouldOpen = !item.classList.contains('is-open')

            navMobilePanel
              .querySelectorAll('.nav-item.is-open')
              .forEach((openItem) => {
                openItem.classList.remove('is-open')
              })

            if (shouldOpen) {
              item.classList.add('is-open')
            }
          })
        })
    }

    document.querySelectorAll('.sortable-submenu').forEach((menu) => {
      ;[...menu.children]
        .sort((a, b) =>
          a.textContent.trim().localeCompare(b.textContent.trim(), 'pt-BR'),
        )
        .forEach((el) => menu.appendChild(el))
    })
  })
})()
