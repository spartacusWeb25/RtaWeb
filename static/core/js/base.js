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
    initInfiniteScroll()
    initResponsiveFilterCollapse()
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
