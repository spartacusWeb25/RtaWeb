from django import forms
from django.core.validators import MaxLengthValidator
from django.db import DatabaseError, ProgrammingError, models

from funcionarios.models import ClassesFuncionario, Funcionarios
from funcionarios.web.choices import BANCOS_CHOICES, BRAZILIAN_UF_CHOICES, COUNTRY_CHOICES


VINCULOS_COMBOBOX_FIELDS = (
    "func_sindicato",
    "func_departamento",
    "func_centro_custo",
    "func_cargo",
    "func_cbo_cargo",
    "func_funcao",
    "func_cbo_funcao",
    "func_acumulacao_cargo",
)

CALCULO_COMBOBOX_FIELDS = (
    "func_tipo_funcionario",
    "func_incidencia_insalubridade",
    "func_incidencia_periculosidade",
    "func_incidencia_adicional_noturno",
    "func_dsr_horas_extras",
    "func_dsr_rendimentos_variaveis",
    "func_dsr_salarios",
)

BANCOS_COMBOBOX_FIELDS = (
)

DECIMAL_FIELDS_META = {
    "func_percentual_fgts": 5,
    "func_rat_aposentadoria": 5,
    "func_horas_mes": 10,
    "func_horas_semana": 10,
    "func_horas_dia": 10,
    "func_salario_base": 15,
    "func_comissao": 5,
    "func_adic_insalubridade": 5,
    "func_adic_periculosidade": 5,
    "func_adicional_noturno": 5,
    "func_vale_alimentacao_compra": 15,
    "func_valor_fixo_adiantamento": 15,
    "func_salario_inicial": 15,
    "func_valor_previdencia_privada": 15,
    "func_valor_previdencia_privada_13": 15,
    "func_base_ir": 15,
    "func_valor_ir": 15,
    "func_base_inss_multiplos_vinculos": 15,
    "func_valor_inss_multiplos_vinculos": 15,
    "func_base_inss_multiplos_vinculos_13": 15,
    "func_valor_inss_multiplos_vinculos_13": 15,
    "func_base_ir_multiplos_vinculos": 15,
    "func_valor_ir_multiplos_vinculos": 15,
    "func_base_ir_multiplos_vinculos_13": 15,
    "func_valor_ir_multiplos_vinculos_13": 15,
}

QUADRO_HORARIOS_COMBOBOX_FIELDS = (
    "func_tipo_revezamento",
    "func_folga_inicial",
)

GRAU_INSTRUCAO_CHOICES = (
    ("", "Selecione"),
    ("01", "01 - Analfabeto, inclusive o que, embora tenha recebido instrucao, nao se alfabetizou"),
    ("02", "02 - Ate o 5o ano incompleto do ensino fundamental (antiga 4a serie) ou que se tenha alfabetizado sem ter frequentado escola regular"),
    ("03", "03 - 5o ano completo do ensino fundamental"),
    ("04", "04 - Do 6o ao 9o ano do ensino fundamental incompleto (antiga 5a a 8a serie)"),
    ("05", "05 - Ensino fundamental completo"),
    ("06", "06 - Ensino medio incompleto"),
    ("07", "07 - Ensino medio completo"),
    ("08", "08 - Educacao superior incompleta"),
    ("09", "09 - Educacao superior completa"),
    ("10", "10 - Pos-graduacao completa"),
    ("11", "11 - Mestrado completo"),
    ("12", "12 - Doutorado completo"),
)

TIPO_SANGUINEO_CHOICES = (
    ("", "Selecione"),
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
)

ETNIA_RACA_CHOICES = (
    ("", "Selecione"),
    (1, "Branca"),
    (2, "Preta"),
    (3, "Parda"),
    (4, "Amarela"),
    (5, "Indígena"),
    (6, "Excluído eSocial - Não informado"),
)

SEXO_CHOICES = (
    ("", "Selecione"),
    ("F", "Feminino"),
    ("M", "Masculino"),
)

COTA_DEFICIENCIA_CHOICES = (
    ("", "Selecione"),
    (1, "Sim"),
    (0, "Não"),
)

TIPO_ADMISSAO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Admissão - reemprego"),
    (2, "2 - Transferência de empresa do mesmo grupo econômico"),
    (3, "3 - Transferência de empresa consorciada ou de consórcio"),
    (4, "4 - Transferência por motivo de sucessão, incorporação, cisão ou fusão"),
    (5, "5 - Reintegração"),
    (6, "6 - Transferência entre matriz e filial"),
    (9, "9 - Outros casos não previstos"),
)

INDICATIVO_ADMISSAO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Normal"),
    (2, "2 - Decorrente de ação fiscal"),
    (3, "3 - Decorrente de decisão judicial"),
)

TIPO_PROVIMENTO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

TIPO_CONTRATO_TRABALHO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Prazo indeterminado"),
    (2, "2 - Prazo determinado, definido em dias"),
    (3, "3 - Prazo determinado, vinculado à ocorrência de um fato"),
)

CATEGORIA_CNH_CHOICES = (
    ("", "Selecione"),
    ("ACC", "ACC"),
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("AB", "AB"),
    ("AC", "AC"),
    ("AD", "AD"),
    ("AE", "AE"),
)

TEMPO_RESIDENCIA_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

CONDICAO_INGRESSO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

ESTADO_CIVIL_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Solteiro(a)"),
    (2, "2 - Casado(a)"),
    (3, "3 - Divorciado(a)"),
    (4, "4 - Separado(a)"),
    (5, "5 - Viúvo(a)"),
)

CATEGORIA_SEFIP_CHOICES = (
    ("", "Selecione"),
    (1, "01 - Empregado"),
    (2, "02 - Trabalhador Avulso"),
    (3, "03 - Trabalhador não vinculado ao RGPS, mas com direito ao FGTS."),
    (4, "04 - Empregado sob contrato de trabalho por prazo determinado (Lei nº 9.601/98)."),
    (5, "05 - Contribuinte Individual - Diretor não empregado com FGTS (Lei nº 8.036/90, art.16)"),
    (6, "06 - Empregado Doméstico"),
    (7, "07 - Menor Aprendiz (Lei 10.097/2000)"),
    (11, "11 - Contribuinte Individual - Diretor não empregado e demais empresários sem FGTS."),
    (12, "12 - Demais Agentes Públicos"),
    (13, "13 - Contribuinte Individual - Trabalhador autônomo ou a este equiparado, inclusive o operador de máquina, com contribuição sobre remuneração cooperado que presta serviço a pessoas físicas, por intermédio da cooperativa de trabalho"),
)

CATEGORIA_ESOCIAL_CHOICES = (
    ("", "Selecione"),
    (101, "101 - Empregado - Geral, inclusive o empregado público da administração direta ou indireta contratado pela CLT"),
    (102, "102 - Empregado - Trabalhador rural por pequeno prazo da Lei 11.718/2008"),
    (103, "103 - Empregado - Aprendiz"),
    (104, "104 - Empregado - Doméstico"),
    (105, "105 - Empregado - Contrato a termo firmado nos termos da Lei 9.601/1998"),
    (106, "106 - Trabalhador temporário - Contrato nos termos da Lei 6.019/1974"),
    (107, "107 - Empregado - Contrato de trabalho Verde e Amarelo - sem acordo para antecipação mensal da multa rescisória do FGTS"),
    (108, "108 - Empregado - Contrato de trabalho Verde e Amarelo - com acordo para antecipação mensal da multa rescisória do FGTS"),
    (111, "111 - Empregado - Contrato de trabalho intermitente"),
    (201, "201 - Trabalhador avulso portuário"),
    (202, "202 - Trabalhador avulso não portuário"),
    (301, "301 - Servidor público titular de cargo efetivo, magistrado, ministro de Tribunal de Contas, conselheiro de Tribunal de Contas e membro do Ministério Público"),
    (302, "302 - Servidor público ocupante de cargo exclusivo em comissão"),
    (303, "303 - Exercente de mandato eletivo"),
    (304, "304 - Servidor público exercente de mandato eletivo, inclusive com exercício de cargo em comissão"),
    (305, "305 - Servidor público indicado para conselho ou órgão deliberativo, na condição de representante do governo, órgão ou entidade da administração pública"),
    (306, "306 - Servidor público contratado por tempo determinado, sujeito a regime administrativo especial definido em lei própria"),
    (307, "307 - Militar dos Estados e Distrito Federal"),
    (308, "308 - Conscrito"),
    (309, "309 - Agente público - Outros"),
    (310, "310 - Servidor público eventual"),
    (311, "311 - Ministros, juízes, procuradores, promotores ou oficiais de justiça à disposição da Justiça Eleitoral"),
    (312, "312 - Auxiliar local"),
    (313, "313 - Servidor público exercente de atividade de instrutoria, curso ou concurso, convocado para pareceres técnicos, depoimentos ou aditância no exterior"),
    (314, "314 - Militar das Forças Armadas"),
    (401, "401 - Dirigente sindical - Informação prestada pelo sindicato"),
    (410, "410 - Trabalhador cedido/exercício em outro órgão/juiz auxiliar - Informação prestada pelo cessionário/destino"),
    (501, "501 - Dirigente sindical - Segurado especial"),
    (701, "701 - Contribuinte individual - Autônomo em geral, exceto se enquadrado em uma das demais categorias de contribuinte individual"),
    (711, "711 - Contribuinte individual - Transportador autônomo de passageiros"),
    (712, "712 - Contribuinte individual - Transportador autônomo de carga"),
    (721, "721 - Contribuinte individual - Diretor não empregado, com FGTS"),
    (722, "722 - Contribuinte individual - Diretor não empregado, sem FGTS"),
    (723, "723 - Contribuinte individual - Empresário, sócio e membro de conselho de administração ou fiscal"),
    (731, "731 - Contribuinte individual - Cooperado que presta serviços por intermédio de cooperativa de trabalho"),
    (734, "734 - Contribuinte individual - Transportador cooperado que presta serviços por intermédio de cooperativa de trabalho"),
    (738, "738 - Contribuinte individual - Cooperado filiado a cooperativa de produção"),
    (741, "741 - Contribuinte individual - Microempreendedor individual"),
    (751, "751 - Contribuinte individual - Magistrado classista temporário da Justiça do Trabalho ou da Justiça Eleitoral que seja aposentado de qualquer regime previdenciário"),
    (761, "761 - Contribuinte individual - Associado eleito para direção de cooperativa, associação ou entidade de classe de qualquer natureza ou finalidade, bem como o síndico ou administrador eleito para exercer atividade de direção condominial, desde que recebam remuneração"),
    (771, "771 - Contribuinte individual - Membro de conselho tutelar, nos termos da Lei 8.069/1990"),
    (781, "781 - Ministro de confissão religiosa ou membro de vida consagrada, de congregação ou de ordem religiosa"),
    (901, "901 - Estagiário"),
    (902, "902 - Médico residente, residente em área profissional de saúde ou médico em curso de formação"),
    (903, "903 - Bolsista"),
    (904, "904 - Participante de curso de formação, como etapa de concurso público, sem vínculo de emprego/estatutário"),
    (906, "906 - Beneficiário do Programa Nacional de Prestação de Serviço Civil Voluntário"),
)

GRAU_RISCO_CHOICES = (
    ("", "Selecione"),
    (0, "0 - Nunca exposto a agente nocivo"),
    (1, "1 - Não exposição a agente nocivo"),
    (2, "2 - Exposição a agente nocivo (aposentadoria especial aos 15 anos de trabalho)"),
    (3, "3 - Exposição a agente nocivo (aposentadoria especial aos 20 anos de trabalho)"),
    (4, "4 - Exposição a agente nocivo (aposentadoria especial aos 25 anos de trabalho)"),
    (5, "5 - Não exposto a agente nocivo (mais de um vínculo)"),
    (6, "6 - Exposição a agente nocivo (aposentadoria especial aos 15 anos de trabalho) (mais de um vínculo)"),
    (7, "7 - Exposição a agente nocivo (aposentadoria especial aos 20 anos de trabalho) (mais de um vínculo)"),
)

REGIME_PREVIDENCIARIO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - RGPS - Regime Geral da Previdência Social"),
    (2, "2 - RPPS - Regime Próprio de Previdência Social - RPPS, Regime dos Parlamentares e Sistema de Proteção dos Militares"),
    (3, "3 - RPPE - Regime Próprio de Previdência Social no Exterior"),
)

REGIME_TRABALHISTA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - CLT - Consolidação das Leis do Trabalho e legislações trabalhistas específicas"),
    (2, "2 - Estatutário/legislações específicas (servidor temporário, militar, agente político, etc.)"),
)

CATEGORIA_ORIGEM_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

REMUNERACAO_CARGO_ELETIVO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

REGIME_TRABALHISTA_ORIGEM_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "1 - CLT - Consolidação das Leis do Trabalho e legislações trabalhistas específicas"),
    (2, "2 - Estatutário/legislações específicas (servidor temporário, militar, agente político, etc.)"),
)

REGIME_PREVIDENCIARIO_ORIGEM_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "1 - RGPS - Regime Geral da Previdência Social"),
    (2, "2 - RPPS - Regime Próprio de Previdência Social - RPPS, Regime dos Parlamentares e Sistema de Proteção dos Militares"),
    (3, "3 - RPPE - Regime Próprio de Previdência Social no Exterior"),
)

PLANO_SEGREGACAO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

TETO_RGPS_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

ABONO_PERMANENCIA_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
)

NATUREZA_OCUPACAO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Empregado em Empresa do setor privado"),
    (2, "2 - Profissional liberal ou Trabalhador sem vínculo empregatício"),
    (3, "3 - Empregador titular ou proprietário de empresa"),
    (4, "4 - Servidor público da administração direta"),
    (5, "5 - Servidor público de autarquia e fundação"),
    (6, "6 - Funcionário de empresa pública de economia mista"),
    (7, "7 - Declarante auferiu rend. capital, inclusive aluguel"),
    (8, "8 - Aposentado ou pensionista"),
    (9, "9 - Outros"),
)

VINCULO_EMPREGATICIO_CHOICES = (
    ("", "Selecione"),
    (10, "10 - Trabalhador urbano vinculado a empregador pessoa jurídica por contrato de trabalho regido pela CLT, por prazo indeterminado."),
    (15, "15 - Trabalhador urbano vinculado a empregador pessoa física por contrato de trabalho regido pela CLT, por prazo indeterminado."),
    (20, "20 - Trabalhador rural vinculado a empregador pessoa jurídica por contrato de trabalho regido pela Lei nº 5.889/73, por prazo indeterminado."),
    (25, "25 - Trabalhador rural vinculado a empregador pessoa física por contrato de trabalho regido pela Lei nº 5.889/73, por prazo indeterminado."),
    (30, "30 - Servidor regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado ao Regime Próprio de Previdência."),
    (31, "31 - Servidor regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado ao Regime Geral de Previdência Social."),
    (35, "35 - Servidor público não-efetivo (demissível ad nutum)."),
    (40, "40 - Trabalhador avulso (trabalho administrado pelo sindicato da categoria ou pelo órgão gestor de mão-de-obra) para o qual é devido depósito de FGTS e ICF 88, art. 7º, inciso III."),
    (50, "50 - Trabalhador temporário, regido pela Lei nº 6.019, de 3 de janeiro de 1974."),
    (55, "55 - Aprendiz contratado na forma dos arts. 429 ou 430 da CLT, com redações dadas pela Lei nº 10.097, de 19 de dezembro de 2000."),
    (60, "60 - Trabalhador urbano vinculado a empregador pessoa jurídica por contrato de trabalho regido pela CLT, por tempo determinado ou obra certa."),
    (65, "65 - Trabalhador urbano vinculado a empregador pessoa física por contrato de trabalho regido pela CLT, por tempo determinado ou obra certa."),
    (70, "70 - Trabalhador rural vinculado a empregador pessoa jurídica por contrato de trabalho regido pela Lei nº 5.889/73, por prazo determinado."),
    (75, "75 - Trabalhador rural vinculado a empregador pessoa física por contrato de trabalho regido pela Lei nº 5.889/73, por prazo determinado."),
    (80, "80 - Diretor sem vínculo empregatício para o qual o empregador tenha optado pelo recolhimento do FGTS."),
    (90, "90 - Contrato de Trabalho por Prazo Determinado, regido pela Lei nº 9.601, de 21 de janeiro de 1998."),
    (95, "95 - Contrato de Trabalho por Tempo Determinado, regido pela Lei nº 8.745, de 9 de dezembro de 1993, com redação dada pela Lei nº 9.849, de 26 de outubro de 1999."),
    (96, "96 - Contrato de Trabalho por Prazo Determinado, regido por Lei Estadual."),
    (97, "97 - Contrato de Trabalho por Prazo Determinado, regido por Lei Municipal."),
)

FORMA_PAGAMENTO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Mensal"),
    (2, "2 - Quinzenal"),
    (3, "3 - Semanal"),
)

TIPO_CONTA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Conta corrente"),
    (2, "2 - Conta poupança"),
    (3, "3 - Conta salário"),
)

MODO_PAGAMENTO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Crédito em conta"),
    (2, "2 - Depósito em conta"),
    (3, "3 - Pix em conta"),
)

REGIME_JORNADA_TRABALHO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Submetidos a horário de trabalho (Cap. II da CLT)"),
    (2, "2 - Atividade externa especificada no Inciso I do Art. 62 da CLT"),
    (3, "3 - Funções especificadas no Inciso II do Art. 62 da CLT"),
    (4, "4 - Teletrabalho, previsto no Inciso III do Art. 62 da CLT"),
)

TIPO_ESCALA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Normal"),
    (2, "2 - Revezamento"),
    (3, "3 - Nenhuma"),
)

ESCALA_CHOICES = (
    ("", "Selecione"),
    ("1", "1 - Normal"),
    ("2", "2 - Revezamento"),
    ("3", "3 - Nenhuma"),
)

DESCANSO_SEMANAL_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Domingo"),
    (2, "2 - Segunda"),
    (3, "3 - Terça"),
    (4, "4 - Quarta"),
    (5, "5 - Quinta"),
    (6, "6 - Sexta"),
    (7, "7 - Sábado"),
    (8, "8 - Conforme escala"),
)

TIPO_JORNADA_ESOCIAL_CHOICES = (
    ("", "Selecione"),
    (0, "0 - Não informado"),
    (1, "1 - Jornada com horário diário fixo"),
    (2, "2 - Jornada com horário diário fixo e folga variável"),
    (3, "3 - Jornada com horário diário fixo e folga fixa (outro dia que não domingo)"),
    (4, "4 - Jornada com horário diário fixo e folga fixa (no domingo)"),
    (5, "5 - Turno ininterrupto de revezamento"),
    (6, "6 - Jornada 12 x 36 (12 horas de trabalho por 36 de descanso)"),
    (9, "9 - Demais jornadas"),
)


def _only_digits(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _to_decimal_2(value):
    text = (str(value or "")).replace(",", ".").strip()
    if not text:
        return None

    neg = False
    if text.startswith("-"):
        neg = True
        text = text[1:]
    elif text.startswith("+"):
        text = text[1:]

    if not text:
        return None

    parts = text.split(".")
    if len(parts) > 2:
        raise ValueError("Valor decimal invalido")
    if len(parts) == 1:
        int_part, dec_part = parts[0], ""
    else:
        int_part, dec_part = parts

    int_part = "".join(ch for ch in int_part if ch.isdigit())
    dec_part = "".join(ch for ch in dec_part if ch.isdigit())

    if not int_part and not dec_part:
        return None

    if len(dec_part) > 2:
        dec_part = dec_part[:2]

    normalized = f"{int_part or '0'}{'.' + dec_part if dec_part else ''}"
    if neg:
        normalized = "-" + normalized

    from decimal import Decimal, InvalidOperation
    try:
        return Decimal(normalized)
    except (InvalidOperation, ValueError):
        raise ValueError("Valor decimal invalido")


def _cpf_valido(value):
    digits = _only_digits(value)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    soma = sum(int(digits[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_1 = 0 if resto == 10 else resto
    if digito_1 != int(digits[9]):
        return False

    soma = sum(int(digits[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_2 = 0 if resto == 10 else resto
    return digito_2 == int(digits[10])


def _pis_valido(value):
    digits = _only_digits(value)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    pesos = (3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    soma = sum(int(digits[i]) * pesos[i] for i in range(10))
    resto = 11 - (soma % 11)
    digito = 0 if resto in (10, 11) else resto
    return digito == int(digits[10])


def _combo_choices_for_value(value):
    choices = [("", "Selecione")]
    if value not in (None, ""):
        value = str(value)
        choices.append((value, f"{value} - {value}"))
    return choices


def _choices_with_current(base_choices, value):
    choices = list(base_choices)
    if value in (None, ""):
        return tuple(choices)

    value = str(value).strip()
    valid_values = {str(choice_value) for choice_value, _ in choices if choice_value not in (None, "")}
    if value not in valid_values:
        choices.append((value, f"{value} - {value}"))
    return tuple(choices)


def _current_field_value(form, field_name):
    value = None
    if form.is_bound:
        value = form.data.get(field_name)
    if value in (None, ""):
        value = form.initial.get(field_name)
    if value in (None, "") and getattr(form.instance, "pk", None):
        value = getattr(form.instance, field_name, None)
    return value


def _valid_choice_values(choices):
    return {str(choice_value) for choice_value, _ in choices if choice_value not in (None, "")}


def _classes_funcionario_choices(db_alias, value=None):
    choices = [("", "Selecione")]

    if db_alias:
        try:
            registros = (
                ClassesFuncionario.objects.using(db_alias)
                .order_by("clas_codi")
                .values_list("clas_codi", "clas_desc")
            )
            for codigo, descricao in registros:
                descricao = (descricao or "").strip()
                choices.append((codigo, f"{codigo} - {descricao or codigo}"))
        except (DatabaseError, ProgrammingError):
            pass

    return _choices_with_current(tuple(choices), value)


FIELD_LABELS = {
    "registro": "Registro",
    "func_empr": "Empresa",
    "func_codi": "Código",
    "func_fili": "Filial",
    "func_admissao_preliminar": "Admissão preliminar",
    "func_integracao_esocial": "Integração eSocial",
    "func_nome": "Nome",
    "func_email": "E-mail",
    "func_ddd": "DDD",
    "func_telefone": "Telefone",
    "func_ddd_celular": "DDD",
    "func_celular": "Celular",
    "func_nascimento": "Nascimento",
    "func_pais_nascimento": "País de nascimento",
    "func_cidade_nascimento": "Cidade de nascimento",
    "func_naturalidade": "Naturalidade",
    "func_grau_instrucao": "Grau de instrução",
    "func_ficha_registro": "Ficha registro",
    "func_livro": "Livro",
    "func_folha": "Folha",
    "func_cartao_ponto": "Cartão ponto",
    "func_matricula_esocial": "Matrícula eSocial",
    "func_cep": "CEP",
    "func_logr": "Logradouro",
    "func_ende": "Endereço",
    "func_ende_nume": "Número",
    "func_ende_comp": "Complemento",
    "func_ende_bair": "Bairro",
    "func_ende_cida": "Cidade",
    "func_ende_uf": "UF",
    "func_foto_3x4": "Foto 3x4",
    "func_tipo_sanguineo": "Tipo sanguíneo",
    "func_etnia_raca": "Etnia/Raça",
    "func_sexo": "Sexo",
    "func_pessoa_com_deficiencia": "Pessoa com deficiência",
    "func_deficiencia_fisica": "Física",
    "func_deficiencia_visual": "Visual",
    "func_deficiencia_auditiva": "Auditiva",
    "func_deficiencia_mental": "Mental",
    "func_deficiencia_intelectual": "Intelectual",
    "func_reabilitado": "Reabilitado",
    "func_cota_deficiencia": "Cota deficiência",
    "func_observacoes_deficiencias": "Observações das deficiências",
    "func_admissao": "Admissão",
    "func_cadastro": "Cadastro",
    "func_inicio_adicional_tempo_servico": "Início adicional tempo de serviço",
    "func_alvara_judicial_contratacao_menores": "Alvará judicial contratação menores",
    "func_numero_processo": "Número do processo",
    "func_tipo_admissao": "Tipo de admissão",
    "func_indicativo_admissao": "Indicativo de admissão",
    "func_data_aposentadoria": "Data aposentadoria",
    "func_nova_data_admissao": "Nova data de admissão",
    "func_numero_processo_rt": "Número do processo RT",
    "func_tipo_provimento": "Tipo de provimento",
    "func_natureza_ocupacao": "Natureza de ocupação",
    "func_empresa_anterior_cnpj_cpf": "Empresa anterior CNPJ/CPF",
    "func_matricula_anterior": "Matrícula anterior",
    "func_data_transferencia": "Data de transferência",
    "func_transferencia_com_onus": "Transferência com ônus",
    "func_data_saida": "Data saída",
    "func_aviso_previo": "Aviso prévio",
    "func_motivo_saida": "Motivo da saída",
    "func_tipo_contrato_trabalho": "Tipo de contrato de trabalho",
    "func_indicativo_contratacao": "Indicativo da contratação",
    "func_prazo_experiencia_dias": "Prazo de experiência (dias)",
    "func_fim_primeiro_prazo": "Fim do 1º prazo",
    "func_termino_ocorrencia_fato": "Término da ocorrência de um fato",
    "func_prorrogacao_dias": "Prorrogação (dias)",
    "func_fim_prorrogacao": "Fim da prorrogação",
    "func_pais_nacionalidade": "País de nacionalidade",
    "func_chegada_brasil": "Chegada ao Brasil",
    "func_casado_brasileiro": "Casado com brasileiro(a)",
    "func_tem_filhos_brasileiros": "Tem filhos brasileiros",
    "func_rne": "RNE",
    "func_orgao_uf_emissao_rne": "Órgão e UF de emissão RNE",
    "func_emissao_rne": "Emissão RNE",
    "func_tempo_residencia": "Tempo de residência",
    "func_condicao_ingresso": "Condição de ingresso",
    "func_cpf": "CPF",
    "func_pis": "PIS",
    "func_emissao_pis": "Emissão PIS",
    "func_rg": "RG",
    "func_orgao_emissor_rg": "Órgão emissor RG",
    "func_uf_rg": "UF RG",
    "func_emissao_rg": "Emissão RG",
    "func_carteira_trabalho": "Carteira de trabalho",
    "func_serie_carteira_trabalho": "Série",
    "func_digito_serie_carteira_trabalho": "Dígito",
    "func_uf_carteira_trabalho": "UF carteira de trabalho",
    "func_emissao_carteira_trabalho": "Emissão carteira de trabalho",
    "func_cnh": "CNH",
    "func_categoria_cnh": "Categoria CNH",
    "func_uf_cnh": "UF CNH",
    "func_emissao_cnh": "Emissão CNH",
    "func_vencimento_cnh": "Vencimento CNH",
    "func_primeira_habilitacao": "Primeira habilitação",
    "func_titulo_eleitor": "Título eleitor",
    "func_zona_titulo_eleitor": "Zona",
    "func_secao_titulo_eleitor": "Seção",
    "func_certificado_reservista": "Certificado de reservista",
    "func_certidao_civil": "Certidão civil",
    "func_tipo_certidao": "Tipo de certidão",
    "func_emissao_certidao": "Emissão certidão",
    "func_termo_matricula": "Termo/Matrícula",
    "func_livro_certidao": "Livro",
    "func_folha_certidao": "Folha",
    "func_cartorio": "Cartório",
    "func_cidade_cartorio": "Cidade",
    "func_uf_cartorio": "UF cartório",
    "func_nome_pai": "Nome do pai",
    "func_nome_mae": "Nome da mãe",
    "func_estado_civil": "Estado civil",
    "func_nome_conjuge": "Nome do cônjuge",
    "func_dependentes": "Dependentes",
    "func_data_opcao": "Data opção",
    "func_categoria_sefip": "Categoria Sefip",
    "func_categoria_esocial": "Categoria eSocial",
    "func_grau_risco": "Grau de risco",
    "func_percentual_fgts": "Percentual FGTS",
    "func_rat_aposentadoria": "RAT aposentadoria (%)",
    "func_regime_previdenciario": "Regime previdenciário",
    "func_regime_trabalhista": "Regime trabalhista",
    "func_categoria_origem": "Categoria origem",
    "func_tipo_origem_inscricao": "Tipo origem inscrição",
    "func_cnpj_origem": "CNPJ origem",
    "func_admissao_origem": "Admissão origem",
    "func_matricula_origem": "Matrícula origem",
    "func_remuneracao_cargo_eletivo": "Remuneração cargo eletivo",
    "func_regime_trabalhista_origem": "Regime trabalhista origem",
    "func_regime_previdenciario_origem": "Regime previdenciário origem",
    "func_plano_segregacao": "Plano de segregação",
    "func_teto_rgps": "Teto RGPS",
    "func_abono_permanencia": "Abono permanência",
    "func_inicio_abono": "Início abono",
    "func_classe": "Classe",
    "func_sindicato": "Sindicato",
    "func_vinculo_empregaticio": "Vínculo empregatício",
    "func_departamento": "Departamento",
    "func_centro_custo": "Centro de custo",
    "func_cargo": "Cargo",
    "func_nivel": "Nível",
    "func_cbo_cargo": "CBO cargo",
    "func_funcao": "Função",
    "func_cbo_funcao": "CBO função",
    "func_acumulacao_cargo": "Acumulação de cargo",
    "func_orgao_classe": "Órgão de classe",
    "func_inscricao_orgao_classe": "Inscrição órgão de classe",
    "func_orgao_uf_emissao_orgao_classe": "Órgão e UF de emissão",
    "func_emissao_orgao_classe": "Emissão órgão de classe",
    "func_validade_orgao_classe": "Validade órgão de classe",
    "func_horas_mes": "Horas mês",
    "func_horas_semana": "Horas semana",
    "func_horas_dia": "Horas dia",
    "func_forma_pagamento": "Forma de pagamento",
    "func_tipo_funcionario": "Tipo de funcionário",
    "func_salario_base": "Salário base",
    "func_comissao": "Comissão %",
    "func_adic_insalubridade": "Adic. insalubridade %",
    "func_incidencia_insalubridade": "Incidência insalubridade",
    "func_adic_periculosidade": "Adic. periculosidade %",
    "func_incidencia_periculosidade": "Incidência periculosidade",
    "func_adicional_noturno": "Adicional noturno %",
    "func_incidencia_adicional_noturno": "Incidência adicional noturno",
    "func_vale_alimentacao_compra": "Valor vale alimentação/compra",
    "func_recebe_dsr_horas_extras": "Recebe DSR sobre horas extras",
    "func_dsr_horas_extras": "DSR H.E.",
    "func_recebe_dsr_rendimentos_variaveis": "Recebe DSR sobre rendimentos variáveis",
    "func_dsr_rendimentos_variaveis": "DSR R.V.",
    "func_recebe_dsr_salarios": "Recebe DSR sobre salários",
    "func_dsr_salarios": "DSR salário",
    "func_ignora_faltas_ferias": "Ignora faltas nas férias",
    "func_imprimir_etiqueta": "Imprimir etiqueta",
    "func_regime_tempo_parcial": "Regime de tempo parcial",
    "func_nao_arredondar": "Não arredondar",
    "func_salario_contratual_comissionado": "Salário contratual comissionado",
    "func_adiantamento": "Adiantamento",
    "func_valor_fixo_adiantamento": "Valor fixo",
    "func_aplica_deducao_mais_benefica_irrf": "Aplica dedução mais benéfica no IRRF",
    "func_recebe_vale_refeicao": "Recebe vale refeição",
    "func_vale_refeicao": "Vale refeição",
    "func_cartao_vale_refeicao": "Cartão vale refeição",
    "func_recebe_vale_alimentacao": "Recebe vale alimentação",
    "func_vale_alimentacao": "Vale alimentação",
    "func_cartao_vale_alimentacao": "Cartão vale alimentação",
    "func_banco": "Banco",
    "func_agencia_pagamento": "Agência para pagamento",
    "func_conta_pagamento": "Conta depósito para pagamento",
    "func_digito_conta_pagamento": "Dígito da conta",
    "func_tipo_conta": "Tipo de conta",
    "func_cartao_salario": "Cartão salário",
    "func_modo_pagamento": "Modo de pagamento",
    "func_aquisicao_ferias": "Aquisição férias",
    "func_salario_inicial": "Salário inicial",
    "func_descontar_contribuicao_sindical": "Descontar contribuição sindical",
    "func_sindicalizado": "Sindicalizado",
    "func_valor_previdencia_privada": "Valor previdência privada",
    "func_valor_previdencia_privada_13": "Valor previdência privada 13",
    "func_base_ir": "Base de IR",
    "func_valor_ir": "Valor de IR",
    "func_base_inss_multiplos_vinculos": "Base de INSS múltiplos vínculos",
    "func_valor_inss_multiplos_vinculos": "Valor de INSS múltiplos vínculos",
    "func_base_inss_multiplos_vinculos_13": "Base de INSS múltiplos vínculos 13",
    "func_valor_inss_multiplos_vinculos_13": "Valor de INSS múltiplos vínculos 13",
    "func_base_ir_multiplos_vinculos": "Base de IR múltiplos vínculos",
    "func_valor_ir_multiplos_vinculos": "Valor de IR múltiplos vínculos",
    "func_base_ir_multiplos_vinculos_13": "Base de IR múltiplos vínculos 13",
    "func_valor_ir_multiplos_vinculos_13": "Valor de IR múltiplos vínculos 13",
    "func_vigencia_quadro_horario": "Vigência",
    "func_regime_jornada_trabalho": "Regime jornada de trabalho",
    "func_tipo_escala": "Tipo de escala",
    "func_pre_assinalar_horarios_intervalo": "Pré-assinalar horários de intervalo",
    "func_escala": "Escala",
    "func_descanso_semanal": "Descanso semanal",
    "func_data_inicio_escala": "Data início escala",
    "func_tipo_revezamento": "Tipo de revezamento",
    "func_tipo_jornada_esocial": "Tipo de jornada eSocial",
    "func_horario_noturno": "Horário noturno",
    "func_folga_inicial": "Folga inicial",
    "func_nit": "NIT",
    "func_qualificacao_cadastral_status": "Status da qualificação cadastral",
    "func_esocial_integrado": "Integrado no eSocial",
    "func_esocial_data_integracao": "Data e hora da integração no eSocial",
    "func_esocial_numero_recibo": "Número do recibo",
    "func_ultimo_exame_medico": "Último exame médico",
    "func_proximo_exame_medico_meses": "Próximo exame (meses) médico",
    "func_proximo_exame_medico": "Próximo exame médico",
    "func_ultimo_exame_audiometrico": "Último exame audiométrico",
    "func_proximo_exame_audiometrico_meses": "Próximo exame (meses) audiométrico",
    "func_proximo_exame_audiometrico": "Próximo exame audiométrico",
    "func_aprendiz_gravida": "Aprendiz grávida",
    "func_observacoes": "Observações",
}


class FuncionarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        super().__init__(*args, **kwargs)

        for nome, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(nome)

            if isinstance(model_field, models.BooleanField):
                field.required = False
                field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
                continue

            if isinstance(model_field, models.DateTimeField):
                field.widget = forms.DateTimeInput(
                    attrs={"class": "form-control", "type": "datetime-local"},
                    format="%Y-%m-%dT%H:%M",
                )
                field.input_formats = ["%Y-%m-%dT%H:%M"]
                continue

            if isinstance(model_field, models.DateField):
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "type": "date"},
                    format="%Y-%m-%d",
                )
                field.input_formats = ["%Y-%m-%d"]
                continue

            if isinstance(model_field, models.TextField):
                field.widget.attrs.setdefault("class", "form-control")
                field.widget.attrs.setdefault("rows", 3)
                continue

            if isinstance(model_field, (models.IntegerField, models.DecimalField)):
                widget = field.widget
                if not isinstance(widget, forms.NumberInput):
                    widget = forms.NumberInput()
                    field.widget = widget
                widget.attrs["class"] = "form-control"
                if isinstance(model_field, models.DecimalField):
                    widget.attrs.setdefault("step", "0.01")
                continue

            if isinstance(model_field, models.BinaryField):
                field.required = False
                field.widget = forms.ClearableFileInput(attrs={"class": "form-control"})
                continue

            field.widget.attrs["class"] = "form-control"

        if "func_tipo_origem_inscricao" in self.fields:
            field = self.fields["func_tipo_origem_inscricao"]
            field.widget = forms.RadioSelect(
                choices=((1, "CNPJ"), (2, "CPF")),
                attrs={"class": "form-check-input"},
            )
            field.required = False

        if "func_grau_instrucao" in self.fields:
            self.fields["func_grau_instrucao"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=GRAU_INSTRUCAO_CHOICES,
            )
            self.fields["func_grau_instrucao"].required = False

        if "func_cpf" in self.fields:
            field = self.fields["func_cpf"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.validators = [validator for validator in field.validators if not isinstance(validator, MaxLengthValidator)]
            field.validators.append(MaxLengthValidator(14))

        if "func_pis" in self.fields:
            field = self.fields["func_pis"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.validators = [validator for validator in field.validators if not isinstance(validator, MaxLengthValidator)]
            field.validators.append(MaxLengthValidator(14))

        if "func_pais_nascimento" in self.fields:
            valor_atual = _current_field_value(self, "func_pais_nascimento")
            self.fields["func_pais_nascimento"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["func_pais_nascimento"].required = False

        if "func_pais_nacionalidade" in self.fields:
            valor_atual = _current_field_value(self, "func_pais_nacionalidade")
            self.fields["func_pais_nacionalidade"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["func_pais_nacionalidade"].required = False

        if "func_naturalidade" in self.fields:
            valor_atual = _current_field_value(self, "func_naturalidade")
            self.fields["func_naturalidade"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(BRAZILIAN_UF_CHOICES, valor_atual),
            )
            self.fields["func_naturalidade"].required = False

        for nome in ("func_uf_rg", "func_uf_carteira_trabalho", "func_uf_cnh", "func_uf_cartorio"):
            if nome not in self.fields:
                continue
            valor_atual = _current_field_value(self, nome)
            self.fields[nome].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(BRAZILIAN_UF_CHOICES, valor_atual),
            )
            self.fields[nome].required = False

        if "func_tipo_sanguineo" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_sanguineo")
            self.fields["func_tipo_sanguineo"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_SANGUINEO_CHOICES, valor_atual),
            )
            self.fields["func_tipo_sanguineo"].required = False

        if "func_etnia_raca" in self.fields:
            valor_atual = _current_field_value(self, "func_etnia_raca")
            self.fields["func_etnia_raca"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(ETNIA_RACA_CHOICES, valor_atual),
            )
            self.fields["func_etnia_raca"].required = False

        if "func_sexo" in self.fields:
            valor_atual = _current_field_value(self, "func_sexo")
            self.fields["func_sexo"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(SEXO_CHOICES, valor_atual),
            )
            self.fields["func_sexo"].required = False

        if "func_cota_deficiencia" in self.fields:
            valor_atual = _current_field_value(self, "func_cota_deficiencia")
            self.fields["func_cota_deficiencia"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COTA_DEFICIENCIA_CHOICES, valor_atual),
            )
            self.fields["func_cota_deficiencia"].required = False

        if "func_tipo_admissao" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_admissao")
            self.fields["func_tipo_admissao"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_ADMISSAO_CHOICES, valor_atual),
            )
            self.fields["func_tipo_admissao"].required = False

        if "func_indicativo_admissao" in self.fields:
            valor_atual = _current_field_value(self, "func_indicativo_admissao")
            self.fields["func_indicativo_admissao"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(INDICATIVO_ADMISSAO_CHOICES, valor_atual),
            )
            self.fields["func_indicativo_admissao"].required = False

        if "func_tipo_provimento" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_provimento")
            self.fields["func_tipo_provimento"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_PROVIMENTO_CHOICES, valor_atual),
            )
            self.fields["func_tipo_provimento"].required = False

        if "func_tipo_contrato_trabalho" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_contrato_trabalho")
            self.fields["func_tipo_contrato_trabalho"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_CONTRATO_TRABALHO_CHOICES, valor_atual),
            )
            self.fields["func_tipo_contrato_trabalho"].required = False

        if "func_tempo_residencia" in self.fields:
            valor_atual = _current_field_value(self, "func_tempo_residencia")
            self.fields["func_tempo_residencia"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TEMPO_RESIDENCIA_CHOICES, valor_atual),
            )
            self.fields["func_tempo_residencia"].required = False

        if "func_condicao_ingresso" in self.fields:
            valor_atual = _current_field_value(self, "func_condicao_ingresso")
            self.fields["func_condicao_ingresso"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CONDICAO_INGRESSO_CHOICES, valor_atual),
            )
            self.fields["func_condicao_ingresso"].required = False

        if "func_natureza_ocupacao" in self.fields:
            valor_atual = _current_field_value(self, "func_natureza_ocupacao")
            self.fields["func_natureza_ocupacao"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(NATUREZA_OCUPACAO_CHOICES, valor_atual),
            )
            self.fields["func_natureza_ocupacao"].required = False

        if "func_categoria_cnh" in self.fields:
            valor_atual = _current_field_value(self, "func_categoria_cnh")
            self.fields["func_categoria_cnh"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_CNH_CHOICES, valor_atual),
            )
            self.fields["func_categoria_cnh"].required = False

        if "func_estado_civil" in self.fields:
            valor_atual = _current_field_value(self, "func_estado_civil")
            self.fields["func_estado_civil"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(ESTADO_CIVIL_CHOICES, valor_atual),
            )
            self.fields["func_estado_civil"].required = False

        if "func_categoria_sefip" in self.fields:
            valor_atual = _current_field_value(self, "func_categoria_sefip")
            self.fields["func_categoria_sefip"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_SEFIP_CHOICES, valor_atual),
            )
            self.fields["func_categoria_sefip"].required = False

        if "func_categoria_esocial" in self.fields:
            valor_atual = _current_field_value(self, "func_categoria_esocial")
            self.fields["func_categoria_esocial"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_ESOCIAL_CHOICES, valor_atual),
            )
            self.fields["func_categoria_esocial"].required = False

        if "func_grau_risco" in self.fields:
            valor_atual = _current_field_value(self, "func_grau_risco")
            self.fields["func_grau_risco"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(GRAU_RISCO_CHOICES, valor_atual),
            )
            self.fields["func_grau_risco"].required = False

        if "func_regime_previdenciario" in self.fields:
            valor_atual = _current_field_value(self, "func_regime_previdenciario")
            self.fields["func_regime_previdenciario"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REGIME_PREVIDENCIARIO_CHOICES, valor_atual),
            )
            self.fields["func_regime_previdenciario"].required = False

        if "func_regime_trabalhista" in self.fields:
            valor_atual = _current_field_value(self, "func_regime_trabalhista")
            self.fields["func_regime_trabalhista"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REGIME_TRABALHISTA_CHOICES, valor_atual),
            )
            self.fields["func_regime_trabalhista"].required = False

        if "func_categoria_origem" in self.fields:
            valor_atual = _current_field_value(self, "func_categoria_origem")
            self.fields["func_categoria_origem"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_ORIGEM_CHOICES, valor_atual),
            )
            self.fields["func_categoria_origem"].required = False

        if "func_remuneracao_cargo_eletivo" in self.fields:
            valor_atual = _current_field_value(self, "func_remuneracao_cargo_eletivo")
            self.fields["func_remuneracao_cargo_eletivo"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REMUNERACAO_CARGO_ELETIVO_CHOICES, valor_atual),
            )
            self.fields["func_remuneracao_cargo_eletivo"].required = False

        if "func_regime_trabalhista_origem" in self.fields:
            valor_atual = _current_field_value(self, "func_regime_trabalhista_origem")
            self.fields["func_regime_trabalhista_origem"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REGIME_TRABALHISTA_ORIGEM_CHOICES, valor_atual),
            )
            self.fields["func_regime_trabalhista_origem"].required = False

        if "func_regime_previdenciario_origem" in self.fields:
            valor_atual = _current_field_value(self, "func_regime_previdenciario_origem")
            self.fields["func_regime_previdenciario_origem"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REGIME_PREVIDENCIARIO_ORIGEM_CHOICES, valor_atual),
            )
            self.fields["func_regime_previdenciario_origem"].required = False

        if "func_plano_segregacao" in self.fields:
            valor_atual = _current_field_value(self, "func_plano_segregacao")
            self.fields["func_plano_segregacao"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(PLANO_SEGREGACAO_CHOICES, valor_atual),
            )
            self.fields["func_plano_segregacao"].required = False

        if "func_teto_rgps" in self.fields:
            valor_atual = _current_field_value(self, "func_teto_rgps")
            self.fields["func_teto_rgps"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TETO_RGPS_CHOICES, valor_atual),
            )
            self.fields["func_teto_rgps"].required = False

        if "func_abono_permanencia" in self.fields:
            valor_atual = _current_field_value(self, "func_abono_permanencia")
            self.fields["func_abono_permanencia"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(ABONO_PERMANENCIA_CHOICES, valor_atual),
            )
            self.fields["func_abono_permanencia"].required = False

        if "func_classe" in self.fields:
            valor_atual = _current_field_value(self, "func_classe")
            self.fields["func_classe"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_classes_funcionario_choices(self.db_alias, valor_atual),
            )
            self.fields["func_classe"].required = False

        if "func_vinculo_empregaticio" in self.fields:
            valor_atual = _current_field_value(self, "func_vinculo_empregaticio")
            self.fields["func_vinculo_empregaticio"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(VINCULO_EMPREGATICIO_CHOICES, valor_atual),
            )
            self.fields["func_vinculo_empregaticio"].required = False

        if "func_forma_pagamento" in self.fields:
            valor_atual = _current_field_value(self, "func_forma_pagamento")
            self.fields["func_forma_pagamento"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(FORMA_PAGAMENTO_CHOICES, valor_atual),
            )
            self.fields["func_forma_pagamento"].required = False

        if "func_banco" in self.fields:
            valor_atual = _current_field_value(self, "func_banco")
            if valor_atual not in (None, ""):
                valor_atual = str(_only_digits(valor_atual)).zfill(3)
            self.fields["func_banco"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(BANCOS_CHOICES, valor_atual),
            )
            self.fields["func_banco"].required = False

        if "func_tipo_conta" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_conta")
            self.fields["func_tipo_conta"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_CONTA_CHOICES, valor_atual),
            )
            self.fields["func_tipo_conta"].required = False

        if "func_modo_pagamento" in self.fields:
            valor_atual = _current_field_value(self, "func_modo_pagamento")
            self.fields["func_modo_pagamento"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(MODO_PAGAMENTO_CHOICES, valor_atual),
            )
            self.fields["func_modo_pagamento"].required = False

        if "func_regime_jornada_trabalho" in self.fields:
            valor_atual = _current_field_value(self, "func_regime_jornada_trabalho")
            self.fields["func_regime_jornada_trabalho"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(REGIME_JORNADA_TRABALHO_CHOICES, valor_atual),
            )
            self.fields["func_regime_jornada_trabalho"].required = False

        if "func_tipo_escala" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_escala")
            self.fields["func_tipo_escala"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_ESCALA_CHOICES, valor_atual),
            )
            self.fields["func_tipo_escala"].required = False

        if "func_escala" in self.fields:
            valor_atual = _current_field_value(self, "func_escala")
            if valor_atual not in (None, ""):
                valor_atual = _only_digits(valor_atual) or str(valor_atual)
            self.fields["func_escala"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(ESCALA_CHOICES, valor_atual),
            )
            self.fields["func_escala"].required = False

        if "func_descanso_semanal" in self.fields:
            valor_atual = _current_field_value(self, "func_descanso_semanal")
            self.fields["func_descanso_semanal"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(DESCANSO_SEMANAL_CHOICES, valor_atual),
            )
            self.fields["func_descanso_semanal"].required = False

        if "func_tipo_jornada_esocial" in self.fields:
            valor_atual = _current_field_value(self, "func_tipo_jornada_esocial")
            self.fields["func_tipo_jornada_esocial"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_JORNADA_ESOCIAL_CHOICES, valor_atual),
            )
            self.fields["func_tipo_jornada_esocial"].required = False

        for nome, max_digits in DECIMAL_FIELDS_META.items():
            if nome not in self.fields:
                continue
            self.fields[nome].widget = forms.TextInput(
                attrs={
                    "class": "form-control",
                    "inputmode": "decimal",
                    "step": "0.01",
                    "data-decimal-2": "true",
                    "maxlength": max_digits + 2,
                    "autocomplete": "off",
                }
            )
            self.fields[nome].required = False

        for nome in VINCULOS_COMBOBOX_FIELDS + CALCULO_COMBOBOX_FIELDS + BANCOS_COMBOBOX_FIELDS + QUADRO_HORARIOS_COMBOBOX_FIELDS:
            if nome not in self.fields:
                continue

            valor_atual = _current_field_value(self, nome)

            self.fields[nome].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_combo_choices_for_value(valor_atual),
            )
            self.fields[nome].required = False

        if "func_esocial_data_integracao" in self.fields:
            self.fields["func_esocial_data_integracao"].input_formats = [
                "%Y-%m-%dT%H:%M",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d %H:%M:%S",
            ]

    class Meta:
        model = Funcionarios
        fields = (
            "func_empr",
            "func_fili",
            "func_codi",
            "func_admissao_preliminar",
            "func_nome",
            "func_email",
            "func_ddd",
            "func_telefone",
            "func_ddd_celular",
            "func_celular",
            "func_nascimento",
            "func_pais_nascimento",
            "func_cidade_nascimento",
            "func_naturalidade",
            "func_grau_instrucao",
            "func_ficha_registro",
            "func_livro",
            "func_folha",
            "func_cartao_ponto",
            "func_matricula_esocial",
            "func_cep",
            "func_logr",
            "func_ende",
            "func_ende_nume",
            "func_ende_comp",
            "func_ende_bair",
            "func_ende_cida",
            "func_ende_uf",
            "func_tipo_sanguineo",
            "func_etnia_raca",
            "func_sexo",
            "func_pessoa_com_deficiencia",
            "func_deficiencia_fisica",
            "func_deficiencia_visual",
            "func_deficiencia_auditiva",
            "func_deficiencia_mental",
            "func_deficiencia_intelectual",
            "func_reabilitado",
            "func_cota_deficiencia",
            "func_observacoes_deficiencias",
            "func_admissao",
            "func_cadastro",
            "func_inicio_adicional_tempo_servico",
            "func_alvara_judicial_contratacao_menores",
            "func_numero_processo",
            "func_tipo_admissao",
            "func_indicativo_admissao",
            "func_data_aposentadoria",
            "func_nova_data_admissao",
            "func_numero_processo_rt",
            "func_tipo_provimento",
            "func_natureza_ocupacao",
            "func_empresa_anterior_cnpj_cpf",
            "func_matricula_anterior",
            "func_data_transferencia",
            "func_transferencia_com_onus",
            "func_data_saida",
            "func_aviso_previo",
            "func_motivo_saida",
            "func_tipo_contrato_trabalho",
            "func_indicativo_contratacao",
            "func_prazo_experiencia_dias",
            "func_fim_primeiro_prazo",
            "func_termino_ocorrencia_fato",
            "func_prorrogacao_dias",
            "func_fim_prorrogacao",
            "func_pais_nacionalidade",
            "func_chegada_brasil",
            "func_casado_brasileiro",
            "func_tem_filhos_brasileiros",
            "func_rne",
            "func_orgao_uf_emissao_rne",
            "func_emissao_rne",
            "func_tempo_residencia",
            "func_condicao_ingresso",
            "func_cpf",
            "func_pis",
            "func_emissao_pis",
            "func_rg",
            "func_orgao_emissor_rg",
            "func_uf_rg",
            "func_emissao_rg",
            "func_carteira_trabalho",
            "func_serie_carteira_trabalho",
            "func_digito_serie_carteira_trabalho",
            "func_uf_carteira_trabalho",
            "func_emissao_carteira_trabalho",
            "func_cnh",
            "func_categoria_cnh",
            "func_uf_cnh",
            "func_emissao_cnh",
            "func_vencimento_cnh",
            "func_primeira_habilitacao",
            "func_titulo_eleitor",
            "func_zona_titulo_eleitor",
            "func_secao_titulo_eleitor",
            "func_certificado_reservista",
            "func_certidao_civil",
            "func_tipo_certidao",
            "func_emissao_certidao",
            "func_termo_matricula",
            "func_livro_certidao",
            "func_folha_certidao",
            "func_cartorio",
            "func_cidade_cartorio",
            "func_uf_cartorio",
            "func_nome_pai",
            "func_nome_mae",
            "func_estado_civil",
            "func_nome_conjuge",
            "func_data_opcao",
            "func_categoria_sefip",
            "func_categoria_esocial",
            "func_grau_risco",
            "func_percentual_fgts",
            "func_rat_aposentadoria",
            "func_regime_previdenciario",
            "func_regime_trabalhista",
            "func_categoria_origem",
            "func_tipo_origem_inscricao",
            "func_cnpj_origem",
            "func_admissao_origem",
            "func_matricula_origem",
            "func_remuneracao_cargo_eletivo",
            "func_regime_trabalhista_origem",
            "func_regime_previdenciario_origem",
            "func_plano_segregacao",
            "func_teto_rgps",
            "func_abono_permanencia",
            "func_inicio_abono",
            "func_classe",
            "func_sindicato",
            "func_vinculo_empregaticio",
            "func_departamento",
            "func_centro_custo",
            "func_cargo",
            "func_nivel",
            "func_cbo_cargo",
            "func_funcao",
            "func_cbo_funcao",
            "func_acumulacao_cargo",
            "func_orgao_classe",
            "func_inscricao_orgao_classe",
            "func_orgao_uf_emissao_orgao_classe",
            "func_emissao_orgao_classe",
            "func_validade_orgao_classe",
            "func_horas_mes",
            "func_horas_semana",
            "func_horas_dia",
            "func_forma_pagamento",
            "func_tipo_funcionario",
            "func_salario_base",
            "func_comissao",
            "func_adic_insalubridade",
            "func_incidencia_insalubridade",
            "func_adic_periculosidade",
            "func_incidencia_periculosidade",
            "func_adicional_noturno",
            "func_incidencia_adicional_noturno",
            "func_vale_alimentacao_compra",
            "func_recebe_dsr_horas_extras",
            "func_dsr_horas_extras",
            "func_recebe_dsr_rendimentos_variaveis",
            "func_dsr_rendimentos_variaveis",
            "func_recebe_dsr_salarios",
            "func_dsr_salarios",
            "func_ignora_faltas_ferias",
            "func_imprimir_etiqueta",
            "func_regime_tempo_parcial",
            "func_nao_arredondar",
            "func_salario_contratual_comissionado",
            "func_adiantamento",
            "func_valor_fixo_adiantamento",
            "func_aplica_deducao_mais_benefica_irrf",
            "func_recebe_vale_refeicao",
            "func_vale_refeicao",
            "func_cartao_vale_refeicao",
            "func_recebe_vale_alimentacao",
            "func_vale_alimentacao",
            "func_cartao_vale_alimentacao",
            "func_banco",
            "func_agencia_pagamento",
            "func_conta_pagamento",
            "func_digito_conta_pagamento",
            "func_tipo_conta",
            "func_cartao_salario",
            "func_modo_pagamento",
            "func_aquisicao_ferias",
            "func_salario_inicial",
            "func_descontar_contribuicao_sindical",
            "func_sindicalizado",
            "func_valor_previdencia_privada",
            "func_valor_previdencia_privada_13",
            "func_base_ir",
            "func_valor_ir",
            "func_base_inss_multiplos_vinculos",
            "func_valor_inss_multiplos_vinculos",
            "func_base_inss_multiplos_vinculos_13",
            "func_valor_inss_multiplos_vinculos_13",
            "func_base_ir_multiplos_vinculos",
            "func_valor_ir_multiplos_vinculos",
            "func_base_ir_multiplos_vinculos_13",
            "func_valor_ir_multiplos_vinculos_13",
            "func_vigencia_quadro_horario",
            "func_regime_jornada_trabalho",
            "func_tipo_escala",
            "func_pre_assinalar_horarios_intervalo",
            "func_escala",
            "func_descanso_semanal",
            "func_data_inicio_escala",
            "func_tipo_revezamento",
            "func_tipo_jornada_esocial",
            "func_horario_noturno",
            "func_folga_inicial",
            "func_nit",
            "func_qualificacao_cadastral_status",
            "func_esocial_integrado",
            "func_esocial_data_integracao",
            "func_esocial_numero_recibo",
            "func_ultimo_exame_medico",
            "func_proximo_exame_medico_meses",
            "func_proximo_exame_medico",
            "func_ultimo_exame_audiometrico",
            "func_proximo_exame_audiometrico_meses",
            "func_proximo_exame_audiometrico",
            "func_aprendiz_gravida",
            "func_observacoes",
        )
        labels = FIELD_LABELS
        widgets = {
            "func_motivo_saida": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "func_indicativo_contratacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "func_observacoes_deficiencias": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "func_qualificacao_cadastral_status": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "func_observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "func_cep": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 8,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                    "autocomplete": "postal-code",
                }
            ),
            "func_ddd": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 4,
                    "inputmode": "numeric",
                    "data-mask": "ddd",
                    "placeholder": "(42)",
                    "autocomplete": "off",
                }
            ),
            "func_telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 9,
                    "inputmode": "numeric",
                    "data-mask": "telefone",
                    "placeholder": "9999-0000",
                    "autocomplete": "off",
                }
            ),
            "func_ddd_celular": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 4,
                    "inputmode": "numeric",
                    "data-mask": "ddd",
                    "placeholder": "(42)",
                    "autocomplete": "off",
                }
            ),
            "func_celular": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 10,
                    "inputmode": "numeric",
                    "data-mask": "celular",
                    "placeholder": "99999-0000",
                    "autocomplete": "off",
                }
            ),
            "func_ende_uf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "style": "text-transform: uppercase;",
                }
            ),
            "func_cpf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 14,
                    "inputmode": "numeric",
                    "data-mask": "cpf",
                    "autocomplete": "off",
                }
            ),
            "func_pis": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 14,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                    "autocomplete": "off",
                }
            ),
            "func_rg": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_orgao_emissor_rg": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_nit": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 14,
                    "inputmode": "numeric",
                    "data-mask": "nis",
                    "autocomplete": "off",
                }
            ),
            "func_esocial_data_integracao": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "func_uf_rg": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "style": "text-transform: uppercase;",
                }
            ),
            "func_carteira_trabalho": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_serie_carteira_trabalho": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 10,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_digito_serie_carteira_trabalho": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_uf_carteira_trabalho": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "style": "text-transform: uppercase;",
                }
            ),
            "func_cnh": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_categoria_cnh": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 5,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_uf_cnh": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "style": "text-transform: uppercase;",
                }
            ),
            "func_titulo_eleitor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_zona_titulo_eleitor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 5,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_secao_titulo_eleitor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 5,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_certificado_reservista": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_certidao_civil": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_termo_matricula": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 50,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_livro_certidao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_folha_certidao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_cartorio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 120,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_cidade_cartorio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 7,
                    "autocomplete": "address-level2",
                }
            ),
            "func_uf_cartorio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 2,
                    "style": "text-transform: uppercase;",
                }
            ),
            "func_cnpj_origem": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 14,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_numero_processo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_numero_processo_rt": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_empresa_anterior_cnpj_cpf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 14,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_matricula_anterior": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_vale_refeicao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 10,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_vale_alimentacao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 10,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_cartao_vale_refeicao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_cartao_vale_alimentacao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_agencia_pagamento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 20,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_conta_pagamento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_digito_conta_pagamento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 5,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
            "func_cartao_salario": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 30,
                    "inputmode": "numeric",
                    "data-digits-only": "true",
                }
            ),
        }

    def clean_func_cpf(self):
        value = (self.cleaned_data.get("func_cpf") or "").strip()
        digits = _only_digits(value)[:11]
        if digits and not _cpf_valido(digits):
            raise forms.ValidationError("Informe um CPF válido.")
        return digits

    def clean_func_pis(self):
        value = (self.cleaned_data.get("func_pis") or "").strip()
        return _only_digits(value)[:14]

    def clean_func_nit(self):
        value = (self.cleaned_data.get("func_nit") or "").strip()
        digits = _only_digits(value)[:11]
        if digits and len(digits) != 11:
            raise forms.ValidationError("Informe um NIT válido com 11 dígitos.")
        return digits

    def clean_func_cep(self):
        value = (self.cleaned_data.get("func_cep") or "").strip()
        digits = _only_digits(value)[:8]
        if digits and len(digits) != 8:
            raise forms.ValidationError("Informe um CEP válido com 8 dígitos.")
        return digits

    def clean_func_ddd(self):
        return _only_digits(self.cleaned_data.get("func_ddd"))[:2]

    def clean_func_telefone(self):
        return _only_digits(self.cleaned_data.get("func_telefone"))[:8]

    def clean_func_ddd_celular(self):
        return _only_digits(self.cleaned_data.get("func_ddd_celular"))[:2]

    def clean_func_celular(self):
        return _only_digits(self.cleaned_data.get("func_celular"))[:9]

    def clean_func_grau_instrucao(self):
        value = (self.cleaned_data.get("func_grau_instrucao") or "").strip()
        valid_values = _valid_choice_values(self.fields["func_grau_instrucao"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione um grau de instrução válido.")
        return value or None

    def clean_func_tipo_sanguineo(self):
        value = (self.cleaned_data.get("func_tipo_sanguineo") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_tipo_sanguineo"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione um tipo sanguíneo válido.")
        return value or None

    def clean_func_etnia_raca(self):
        value = self.cleaned_data.get("func_etnia_raca")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_etnia_raca"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma etnia/raça válida.")
        return value

    def clean_func_sexo(self):
        value = (self.cleaned_data.get("func_sexo") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_sexo"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione um sexo válido.")
        return value or None

    def clean_func_cota_deficiencia(self):
        value = self.cleaned_data.get("func_cota_deficiencia")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_cota_deficiencia"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma cota de deficiência válida.")
        return value

    def clean_func_tipo_admissao(self):
        value = self.cleaned_data.get("func_tipo_admissao")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_admissao"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de admissão válido.")
        return value

    def clean_func_indicativo_admissao(self):
        value = self.cleaned_data.get("func_indicativo_admissao")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_indicativo_admissao"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um indicativo de admissão válido.")
        return value

    def clean_func_tipo_provimento(self):
        value = self.cleaned_data.get("func_tipo_provimento")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_provimento"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de provimento válido.")
        return value

    def clean_func_tipo_contrato_trabalho(self):
        value = self.cleaned_data.get("func_tipo_contrato_trabalho")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_contrato_trabalho"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de contrato de trabalho válido.")
        return value

    def clean_func_tempo_residencia(self):
        value = self.cleaned_data.get("func_tempo_residencia")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tempo_residencia"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tempo de residência válido.")
        return value

    def clean_func_condicao_ingresso(self):
        value = self.cleaned_data.get("func_condicao_ingresso")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_condicao_ingresso"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma condição de ingresso válida.")
        return value

    def clean_func_natureza_ocupacao(self):
        value = self.cleaned_data.get("func_natureza_ocupacao")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_natureza_ocupacao"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma natureza de ocupação válida.")
        return value

    def clean_func_estado_civil(self):
        value = self.cleaned_data.get("func_estado_civil")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_estado_civil"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um estado civil válido.")
        return value

    def clean_func_categoria_sefip(self):
        value = self.cleaned_data.get("func_categoria_sefip")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_categoria_sefip"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma categoria Sefip válida.")
        return value

    def clean_func_categoria_esocial(self):
        value = self.cleaned_data.get("func_categoria_esocial")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_categoria_esocial"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma categoria eSocial válida.")
        return value

    def clean_func_grau_risco(self):
        value = self.cleaned_data.get("func_grau_risco")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_grau_risco"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um grau de risco válido.")
        return value

    def clean_func_regime_previdenciario(self):
        value = self.cleaned_data.get("func_regime_previdenciario")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_regime_previdenciario"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um regime previdenciário válido.")
        return value

    def clean_func_regime_trabalhista(self):
        value = self.cleaned_data.get("func_regime_trabalhista")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_regime_trabalhista"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um regime trabalhista válido.")
        return value

    def clean_func_categoria_origem(self):
        value = self.cleaned_data.get("func_categoria_origem")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_categoria_origem"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma categoria de origem válida.")
        return value

    def clean_func_remuneracao_cargo_eletivo(self):
        value = self.cleaned_data.get("func_remuneracao_cargo_eletivo")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_remuneracao_cargo_eletivo"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma remuneração de cargo eletivo válida.")
        return value

    def clean_func_regime_trabalhista_origem(self):
        value = self.cleaned_data.get("func_regime_trabalhista_origem")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_regime_trabalhista_origem"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um regime trabalhista de origem válido.")
        return value

    def clean_func_regime_previdenciario_origem(self):
        value = self.cleaned_data.get("func_regime_previdenciario_origem")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_regime_previdenciario_origem"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um regime previdenciário de origem válido.")
        return value

    def clean_func_plano_segregacao(self):
        value = self.cleaned_data.get("func_plano_segregacao")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_plano_segregacao"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um plano de segregação válido.")
        return value

    def clean_func_teto_rgps(self):
        value = self.cleaned_data.get("func_teto_rgps")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_teto_rgps"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um teto RGPS válido.")
        return value

    def clean_func_abono_permanencia(self):
        value = self.cleaned_data.get("func_abono_permanencia")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_abono_permanencia"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um abono permanência válido.")
        return value

    def clean_func_classe(self):
        value = self.cleaned_data.get("func_classe")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_classe"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma classe válida.")
        return value

    def clean_func_vinculo_empregaticio(self):
        value = self.cleaned_data.get("func_vinculo_empregaticio")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_vinculo_empregaticio"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um vínculo empregatício válido.")
        return value

    def clean_func_forma_pagamento(self):
        value = self.cleaned_data.get("func_forma_pagamento")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_forma_pagamento"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma forma de pagamento válida.")
        return value

    def clean_func_banco(self):
        value = _only_digits(self.cleaned_data.get("func_banco"))
        if not value:
            return None
        value = value.zfill(3)[:6]
        valid_values = _valid_choice_values(self.fields["func_banco"].widget.choices)
        if value not in valid_values:
            raise forms.ValidationError("Selecione um banco válido.")
        return value

    def clean_func_tipo_conta(self):
        value = self.cleaned_data.get("func_tipo_conta")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_conta"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de conta válido.")
        return value

    def clean_func_modo_pagamento(self):
        value = self.cleaned_data.get("func_modo_pagamento")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_modo_pagamento"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um modo de pagamento válido.")
        return value

    def clean_func_regime_jornada_trabalho(self):
        value = self.cleaned_data.get("func_regime_jornada_trabalho")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_regime_jornada_trabalho"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um regime de jornada válido.")
        return value

    def clean_func_tipo_escala(self):
        value = self.cleaned_data.get("func_tipo_escala")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_escala"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de escala válido.")
        return value

    def clean_func_escala(self):
        value = self.cleaned_data.get("func_escala")
        if value in (None, ""):
            return None
        value = _only_digits(value) or str(value).strip()
        valid_values = _valid_choice_values(self.fields["func_escala"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione uma escala válida.")
        return value

    def clean_func_descanso_semanal(self):
        value = self.cleaned_data.get("func_descanso_semanal")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_descanso_semanal"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um descanso semanal válido.")
        return value

    def clean_func_tipo_jornada_esocial(self):
        value = self.cleaned_data.get("func_tipo_jornada_esocial")
        if value in (None, ""):
            return None
        valid_values = _valid_choice_values(self.fields["func_tipo_jornada_esocial"].widget.choices)
        if str(value) not in valid_values:
            raise forms.ValidationError("Selecione um tipo de jornada eSocial válido.")
        return value

    def clean_func_agencia_pagamento(self):
        value = _only_digits(self.cleaned_data.get("func_agencia_pagamento"))
        return value[:20] or None

    def clean_func_conta_pagamento(self):
        value = _only_digits(self.cleaned_data.get("func_conta_pagamento"))
        return value[:30] or None

    def clean_func_digito_conta_pagamento(self):
        value = _only_digits(self.cleaned_data.get("func_digito_conta_pagamento"))
        return value[:5] or None

    def clean_func_cartao_salario(self):
        value = _only_digits(self.cleaned_data.get("func_cartao_salario"))
        return value[:30] or None

    def clean_func_vale_refeicao(self):
        value = _only_digits(self.cleaned_data.get("func_vale_refeicao"))
        if not value:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            raise forms.ValidationError("Informe um valor numérico válido para vale refeição.")

    def clean_func_vale_alimentacao(self):
        value = _only_digits(self.cleaned_data.get("func_vale_alimentacao"))
        if not value:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            raise forms.ValidationError("Informe um valor numérico válido para vale alimentação.")

    def clean_func_cartao_vale_refeicao(self):
        value = _only_digits(self.cleaned_data.get("func_cartao_vale_refeicao"))
        return value[:30] or None

    def clean_func_cartao_vale_alimentacao(self):
        value = _only_digits(self.cleaned_data.get("func_cartao_vale_alimentacao"))
        return value[:30] or None

    def clean_func_pais_nascimento(self):
        value = (self.cleaned_data.get("func_pais_nascimento") or "").strip()
        valid_values = _valid_choice_values(self.fields["func_pais_nascimento"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione um país de nascimento válido.")
        return value or None

    def clean_func_pais_nacionalidade(self):
        value = (self.cleaned_data.get("func_pais_nacionalidade") or "").strip()
        valid_values = _valid_choice_values(self.fields["func_pais_nacionalidade"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione um país de nacionalidade válido.")
        return value or None

    def clean_func_naturalidade(self):
        value = (self.cleaned_data.get("func_naturalidade") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_naturalidade"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma naturalidade válida.")
        return value or None

    def clean_func_ende_uf(self):
        value = (self.cleaned_data.get("func_ende_uf") or "").strip().upper()
        return value[:2]

    def clean_func_uf_rg(self):
        value = (self.cleaned_data.get("func_uf_rg") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_uf_rg"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma UF do RG válida.")
        return value or None

    def clean_func_uf_carteira_trabalho(self):
        value = (self.cleaned_data.get("func_uf_carteira_trabalho") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_uf_carteira_trabalho"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma UF da carteira de trabalho válida.")
        return value or None

    def clean_func_categoria_cnh(self):
        value = (self.cleaned_data.get("func_categoria_cnh") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_categoria_cnh"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma categoria de CNH válida.")
        return value or None

    def clean_func_uf_cnh(self):
        value = (self.cleaned_data.get("func_uf_cnh") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_uf_cnh"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma UF da CNH válida.")
        return value or None

    def clean_func_uf_cartorio(self):
        value = (self.cleaned_data.get("func_uf_cartorio") or "").strip().upper()
        valid_values = _valid_choice_values(self.fields["func_uf_cartorio"].widget.choices)
        if value and value not in valid_values:
            raise forms.ValidationError("Selecione uma UF do cartório válida.")
        return value or None

    def clean_func_rg(self):
        return _only_digits(self.cleaned_data.get("func_rg"))[:20]

    def clean_func_orgao_emissor_rg(self):
        return _only_digits(self.cleaned_data.get("func_orgao_emissor_rg"))[:20]

    def clean_func_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("func_carteira_trabalho"))[:20]

    def clean_func_serie_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("func_serie_carteira_trabalho"))[:10]

    def clean_func_digito_serie_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("func_digito_serie_carteira_trabalho"))[:2]

    def clean_func_cnh(self):
        return _only_digits(self.cleaned_data.get("func_cnh"))[:20]

    def clean_func_numero_processo(self):
        return _only_digits(self.cleaned_data.get("func_numero_processo"))[:30]

    def clean_func_numero_processo_rt(self):
        return _only_digits(self.cleaned_data.get("func_numero_processo_rt"))[:30]

    def clean_func_empresa_anterior_cnpj_cpf(self):
        return _only_digits(self.cleaned_data.get("func_empresa_anterior_cnpj_cpf"))[:14]

    def clean_func_matricula_anterior(self):
        return _only_digits(self.cleaned_data.get("func_matricula_anterior"))[:30]

    def clean_func_titulo_eleitor(self):
        return _only_digits(self.cleaned_data.get("func_titulo_eleitor"))[:20]

    def clean_func_zona_titulo_eleitor(self):
        return _only_digits(self.cleaned_data.get("func_zona_titulo_eleitor"))[:5]

    def clean_func_secao_titulo_eleitor(self):
        return _only_digits(self.cleaned_data.get("func_secao_titulo_eleitor"))[:5]

    def clean_func_cidade_cartorio(self):
        value = (self.cleaned_data.get("func_cidade_cartorio") or "").strip()
        return value[:7] or None

    def clean_func_certificado_reservista(self):
        return _only_digits(self.cleaned_data.get("func_certificado_reservista"))[:30]

    def clean_func_certidao_civil(self):
        return _only_digits(self.cleaned_data.get("func_certidao_civil"))[:30]

    def clean_func_termo_matricula(self):
        return _only_digits(self.cleaned_data.get("func_termo_matricula"))[:50]

    def clean_func_livro_certidao(self):
        return _only_digits(self.cleaned_data.get("func_livro_certidao"))[:20]

    def clean_func_folha_certidao(self):
        return _only_digits(self.cleaned_data.get("func_folha_certidao"))[:20]

    def clean_func_cartorio(self):
        return _only_digits(self.cleaned_data.get("func_cartorio"))[:120]

    def clean_func_cnpj_origem(self):
        digits = _only_digits(self.cleaned_data.get("func_cnpj_origem"))
        tipo = self.cleaned_data.get("func_tipo_origem_inscricao")

        if digits:
            if str(tipo) == "2":
                digits = digits[:11]
                if len(digits) != 11:
                    raise forms.ValidationError("Informe um CPF válido com 11 dígitos.")
            else:
                digits = digits[:14]
                if len(digits) != 14:
                    raise forms.ValidationError("Informe um CNPJ válido com 14 dígitos.")

        return digits

    def clean(self):
        cleaned_data = super().clean()
        for campo in DECIMAL_FIELDS_META:
            if campo not in cleaned_data:
                continue
            raw = cleaned_data.get(campo)
            if raw in (None, ""):
                cleaned_data[campo] = None
                continue
            try:
                cleaned_data[campo] = _to_decimal_2(raw)
            except ValueError:
                self.add_error(
                    campo,
                    forms.ValidationError(
                        "Informe um valor decimal válido com até 2 casas decimais."
                    ),
                )
        for campo in (
            "func_cpf",
            "func_pis",
            "func_nit",
            "func_cep",
            "func_ddd",
            "func_telefone",
            "func_ddd_celular",
            "func_celular",
            "func_pais_nascimento",
            "func_pais_nacionalidade",
            "func_naturalidade",
            "func_grau_instrucao",
            "func_tipo_sanguineo",
            "func_etnia_raca",
            "func_sexo",
            "func_cota_deficiencia",
            "func_tipo_admissao",
            "func_indicativo_admissao",
            "func_tipo_provimento",
            "func_tipo_contrato_trabalho",
            "func_tempo_residencia",
            "func_condicao_ingresso",
            "func_natureza_ocupacao",
            "func_ende_uf",
            "func_uf_rg",
            "func_uf_carteira_trabalho",
            "func_uf_cnh",
            "func_uf_cartorio",
            "func_carteira_trabalho",
            "func_serie_carteira_trabalho",
            "func_digito_serie_carteira_trabalho",
            "func_cnh",
            "func_titulo_eleitor",
            "func_zona_titulo_eleitor",
            "func_secao_titulo_eleitor",
            "func_cidade_cartorio",
            "func_cnpj_origem",
        ):
            valor = cleaned_data.get(campo)
            if valor == "":
                cleaned_data[campo] = None
        return cleaned_data
