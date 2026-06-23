import re
# Funções de utilitário para manipulação de referências de mês/ano nas referencias da folha de pagamento


DEFAULT_BANCO_SLUG = "rta0001"
REFERENCIA_DISPLAY_RE = re.compile(r"^(0[1-9]|1[0-2])/\d{4}$")
REFERENCIA_STORAGE_RE = re.compile(r"^\d{6}$")
MIN_REFERENCE_YEAR = 1900
MAX_REFERENCE_YEAR = 2999


def _is_valid_reference_year(year):
    if not year or not str(year).isdigit():
        return False
    return MIN_REFERENCE_YEAR <= int(year) <= MAX_REFERENCE_YEAR


def get_db_from_slug(_slug=None):
    """
    Cenário atual: dados operacionais sempre no banco default.
    Mantemos a função por compatibilidade com o padrão do projeto.
    """
    return "default"


def get_default_banco_slug():
    return DEFAULT_BANCO_SLUG


def normalize_month_reference(value, *, strict=False):
    if value is None:
        return value

    value = str(value).strip()
    if not value:
        return ""

    if REFERENCIA_STORAGE_RE.fullmatch(value):
        year = value[:4]
        month = value[4:6]
        if "01" <= month <= "12" and _is_valid_reference_year(year):
            return value
        if strict:
            raise ValueError("Informe a referência no formato MM/AAAA com ano válido.")
        return value

    if REFERENCIA_DISPLAY_RE.fullmatch(value):
        month, year = value.split("/")
        if _is_valid_reference_year(year):
            return f"{year}{month}"
        if strict:
            raise ValueError("Informe a referência no formato MM/AAAA com ano válido.")
        return value

    if strict:
        raise ValueError("Informe a referência no formato MM/AAAA.")

    return value


def get_month_reference_search_terms(value):
    value = normalize_month_reference(value)
    if not value:
        return []

    terms = [value]

    if REFERENCIA_STORAGE_RE.fullmatch(value):
        month = value[4:6]
        if "01" <= month <= "12":
            legacy_value = f"{month}{value[:4]}"
            if legacy_value != value:
                terms.append(legacy_value)

    return terms


def format_month_reference(value):
    if value is None:
        return ""

    value = str(value).strip()
    if not value:
        return ""

    if REFERENCIA_STORAGE_RE.fullmatch(value):
        month = value[4:6]
        if "01" <= month <= "12":
            return f"{month}/{value[:4]}"

        legacy_month = value[:2]
        legacy_year = value[2:6]
        if "01" <= legacy_month <= "12":
            return f"{legacy_month}/{legacy_year}"

    if REFERENCIA_DISPLAY_RE.fullmatch(value):
        return value

    return value
