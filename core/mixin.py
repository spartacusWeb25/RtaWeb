from django.http import Http404
from core.banco import get_banco_from_request
from core.utils import get_db_from_slug


class BancoObrigatorioMixin:
    def dispatch(self, request, *args, **kwargs):
        request.banco = get_banco_from_request(request)
        request.db_alias = get_db_from_slug(request.banco)

        return super().dispatch(request, *args, **kwargs)

    def get_banco_lookup(self):
        return {"registro": self.request.banco}

    def get_contextual_object(self, queryset, **lookup):
        filtros = self.get_banco_lookup()
        filtros.update(lookup)

        objeto = queryset.using(self.request.db_alias).filter(**filtros).first()

        if not objeto:
            raise Http404("Registro não encontrado.")

        return objeto


class InfiniteScrollMixin:
    infinite_scroll_items_selector = "[data-infinite-scroll-items]"
    infinite_scroll_page_param = "page"

    def get_infinite_scroll_next_url(self, page_number: int) -> str:
        params = self.request.GET.copy()
        params[self.infinite_scroll_page_param] = str(page_number)
        query = params.urlencode()

        if query:
            return f"{self.request.path}?{query}"
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = context.get("page_obj")
        is_paginated = bool(context.get("is_paginated"))

        if is_paginated and page_obj and page_obj.has_next():
            context["infinite_scroll_next_url"] = self.get_infinite_scroll_next_url(
                page_obj.next_page_number()
            )
        else:
            context["infinite_scroll_next_url"] = ""

        context["infinite_scroll_items_selector"] = self.infinite_scroll_items_selector
        return context
