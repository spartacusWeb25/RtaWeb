TIPO_REFERENCIA_CHOICES = (
    ("", "Selecione"),
    (1, "Valor"),
    (2, "Percentual"),
    (3, "Avos"),
    (4, "Dia"),
    (5, "Hora"),
    (6, "Mês"),
)

TIPO_VERBA_CHOICES = (
    ("", "Selecione"),
    (1, "Provento"),
    (2, "Desconto"),
    (4, "Informativa"),
)

NATUREZA_RUBRICA_CHOICES = (
    ("", "Selecione"),
    ("101", "101 - Salário base"),
    ("102", "102 - Comissões"),
    ("103", "103 - Bonificações"),
    ("104", "104 - Adicionais"),
    ("105", "105 - Horas extras"),
    ("106", "106 - Gratificações"),
    ("107", "107 - Auxílios"),
    ("108", "108 - Diárias"),
    ("109", "109 - Ajuda de custo"),
    ("110", "110 - Indenizações"),
    ("201", "201 - Previdência oficial"),
    ("202", "202 - Imposto de renda"),
    ("203", "203 - FGTS"),
    ("204", "204 - Contribuição sindical"),
    ("205", "205 - Descontos diversos"),
    ("206", "206 - Pensão alimentícia"),
    ("207", "207 - Previdência privada"),
    ("301", "301 - Bases de cálculo"),
    ("901", "901 - Outras provisões"),
    ("902", "902 - Outros descontos"),
    ("9933", "9933 - Auxílio-doença"),
)

ESOCIAL_CODIGO_CHOICES = (
    ("", "Selecione"),
    ("00", "00 - Não é base de cálculo"),
    ("09", "09 - Verba transitada pela folha de pagamento"),
    ("51", "51 - Salário-família: Outros"),
)

TETO_REMUNERATORIO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "Limite do Teto Constitucional"),
    (2, "Limite do Teto do Regime"),
)

INCIDENCIA_CPRP_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado: CPRP"),
    (1, "Incide CPRP"),
    (2, "Não incide CPRP"),
)

FUNCIONARIOS_AFASTADOS_CHOICES = (
    ("", "Selecione"),
    (0, "Calcula normal"),
    (1, "Não calcula"),
    (2, "Calcula parcial"),
)

EVEN_TIPO_CHOICES = (
    ("", "Selecione"),
    ("P", "Provento"),
    ("D", "Desconto"),
    ("N", "Neutro"),
    ("B", "Base"),
)

EVEN_DERE_CHOICES = (
    ("", "Selecione"),
    ("01", "01 - Normal"),
    ("02", "02 - 13º Salário"),
    ("03", "03 - Férias"),
    ("04", "04 - Rescisão"),
    ("05", "05 - Aviso Prévio"),
)
