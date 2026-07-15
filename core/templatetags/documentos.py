from django import template


register = template.Library()


def _only_digits(value):
    if value in (None, ""):
        return ""
    return "".join(ch for ch in str(value) if ch.isdigit())


@register.filter
def format_cnpj(value):
    digits = _only_digits(value)
    if len(digits) != 14:
        return value or "-"
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"


@register.filter
def format_cpf(value):
    digits = _only_digits(value)
    if len(digits) != 11:
        return value or "-"
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
