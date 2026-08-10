from django import template
from dependentesrh.web.choices import _TOP_CIDADES_IBGE

register = template.Library()


@register.simple_tag()
def cidades_ibge_options():
    items = []
    for codigo, nome, uf in _TOP_CIDADES_IBGE:
        try:
            codigo_num = int(codigo)
        except Exception:
            continue
        items.append(
            f'<option value="{codigo:0>7} — {nome} / {uf}" '
            f'data-codigo="{codigo_num}" data-nome="{nome}" data-uf="{uf}">'
        )
    return "".join(items)
