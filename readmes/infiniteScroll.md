Infinite Scroll (componente + mixin no core)

- Criei o componente reutilizável em: infinite_scroll.html
- Criei o mixin reutilizável em: mixin.py ( InfiniteScrollMixin ) que injeta infinite_scroll_next_url e infinite_scroll_items_selector .
- Ativei no listar de setores (pra validar agora):
  - View usando o mixin: setores/web/views/listar.py
  - Template com data-infinite-scroll-items e include do componente: setores/listar.html
- JS global que faz o carregamento automático das próximas páginas: base.js
- Estilo do status/sentinel: list.css
Agora, em qualquer listar com paginate_by , pra habilitar é só:

- Herdar InfiniteScrollMixin na ListView
- Marcar o container de itens com data-infinite-scroll-items
- Incluir {% include "partials/componentes/infinite_scroll.html" %} no final da listagem.