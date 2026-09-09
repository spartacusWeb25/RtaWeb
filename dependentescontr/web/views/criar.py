from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from dependentescontr.web.forms import DependentescontrForm
from dependentescontr.services.criar import DependentescontrCriarService
from dependentescontr.services.chave import DependentescontrChaveService
from dependentescontr.choices import _TOP_CIDADES_IBGE
from dependentescontr.services.logic import DependentescontrService
from empresas.models import Empresas


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _buscar_contribuintes_por_empfili(db_alias, banco):
    banco_limpo = _digits_only(banco)
    contribuintes_por_empfili = {}
    try:
        from contribuintes.models import Contribuintes
        from contribuintes.services.listar import ListarContribuintesService
        try:
            contribuintes = ListarContribuintesService.listar(
                banco=banco_limpo,
                db_alias=db_alias,
            ) or []
        except Exception:
            contribuintes = (
                Contribuintes.objects.using(db_alias)
                .filter(registro=banco_limpo)
                .all()
            )
        for contr_obj in list(contribuintes):
            try:
                cempr = int(getattr(contr_obj, "contr_empr", 0) or 0)
                cfili = int(getattr(contr_obj, "contr_fili", 0) or 0)
                codc = int(getattr(contr_obj, "contr_codi", 0) or 0)
                nomec = getattr(contr_obj, "contr_nome", "") or "Sem nome"
            except Exception:
                continue
            if not cempr or not cfili or not codc:
                continue
            chave = f"{cempr}_{cfili}"
            if chave not in contribuintes_por_empfili:
                contribuintes_por_empfili[chave] = []
            contribuintes_por_empfili[chave].append((str(codc), f"{codc} — {nomec}"))
    except Exception:
        pass

    for chave, lista in contribuintes_por_empfili.items():
        lista.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        contribuintes_por_empfili[chave] = [("", "Selecione...")] + lista
    return contribuintes_por_empfili


def _obter_contexto_contribuinte(request, empresa, filial, contribuinte):
    if not empresa or not filial or not contribuinte:
        return None
    try:
        from contribuintes.models import Contribuintes
        from empresas.models import Empresas
        banco_limpo = _digits_only(request.banco)

        dados = {
            "contribuinte": None,
            "empresa_nome": "",
            "empresa": empresa,
            "filial": filial,
            "empresa_display": "",
            "filial_display": "",
            "contribuinte_display": "",
        }

        emp = (
            Empresas.objects.using(request.db_alias)
            .filter(registro=banco_limpo, empr_empr=int(empresa), empr_fili=1)
            .values("empr_nome")
            .first()
        )
        if emp:
            dados["empresa_nome"] = emp["empr_nome"]
            dados["empresa_display"] = f"{empresa} — {emp['empr_nome']}"
        else:
            dados["empresa_display"] = str(empresa)

        fil = (
            Empresas.objects.using(request.db_alias)
            .filter(registro=banco_limpo, empr_empr=int(empresa), empr_fili=int(filial))
            .values("empr_nome")
            .first()
        )
        if fil:
            dados["filial_display"] = f"{filial} — {fil['empr_nome']}"
        else:
            dados["filial_display"] = str(filial)

        contr = (
            Contribuintes.objects.using(request.db_alias)
            .filter(
                registro=banco_limpo,
                contr_empr=int(empresa),
                contr_fili=int(filial),
                contr_codi=int(contribuinte),
            )
            .values("contr_codi", "contr_nome", "contr_cpf", "contr_empr", "contr_fili", "contr_admissao")
            .first()
        )
        if contr:
            dados["contribuinte"] = contr
            dados["contribuinte_display"] = str(contr["contr_codi"])
        else:
            dados["contribuinte_display"] = str(contribuinte)

        return dados
    except Exception:
        return None


def _obter_empresa_padrao_e_filiais(db_alias, banco):
    banco_limpo = _digits_only(banco)
    empresa_padrao = None
    try:
        empresa_padrao = DependentescontrService.obter_empresa_padrao(
            banco=banco_limpo, db_alias=db_alias
        )
    except Exception:
        empresa_padrao = None
    empr_padrao_cod = int(getattr(empresa_padrao, "empr_empr", 1) or 1)
    fili_padrao_cod = int(getattr(empresa_padrao, "empr_fili", 1) or 1)

    linhas_filiais = []
    try:
        qs = (
            Empresas.objects.using(db_alias)
            .filter(registro=banco_limpo)
            .order_by("empr_empr", "empr_fili")
        )
        for emp in list(qs):
            try:
                e_empr = int(getattr(emp, "empr_empr", 0) or 0)
                e_fili = int(getattr(emp, "empr_fili", 0) or 0)
                e_nome = (getattr(emp, "empr_nome", "") or "").strip() or f"Empresa {e_empr}"
                linhas_filiais.append((e_empr, e_fili, e_nome))
            except Exception:
                continue
    except Exception:
        linhas_filiais = []

    if not linhas_filiais:
        linhas_filiais.append((empr_padrao_cod, fili_padrao_cod, "Empresa"))

    filiais_da_empresa_logada = []
    for (empr_c, fili_c, nome_c) in linhas_filiais:
        if empr_c == empr_padrao_cod:
            filiais_da_empresa_logada.append((empr_c, fili_c, nome_c))

    vals_fili = [f for (_, f, _) in filiais_da_empresa_logada]
    if len(vals_fili) >= 2 and len(set(vals_fili)) == 1:
        corrigidas = []
        for pos, (empr_c, _fili_antigo, nome_c) in enumerate(filiais_da_empresa_logada, start=1):
            corrigidas.append((empr_c, pos, nome_c))
        filiais_da_empresa_logada = corrigidas

    if not filiais_da_empresa_logada:
        filiais_da_empresa_logada = [(empr_padrao_cod, fili_padrao_cod, "Empresa")]

    return (empresa_padrao, empr_padrao_cod, fili_padrao_cod, filiais_da_empresa_logada)


def _montar_mapas_dinamicos(db_alias, banco):
    (
        empresa_padrao,
        empr_padrao_cod,
        fili_padrao_cod,
        filiais_da_empresa_logada,
    ) = _obter_empresa_padrao_e_filiais(db_alias, banco)

    choices_empresa_combo = [("", "Selecione...")]
    for (empr_c, fili_c, nome_c) in filiais_da_empresa_logada:
        choices_empresa_combo.append((str(fili_c), f"{empr_c} — {nome_c}"))

    contribuintes_por_empfili = _buscar_contribuintes_por_empfili(db_alias, banco)

    for (empr_c, fili_c, _) in filiais_da_empresa_logada:
        chave = f"{empr_c}_{fili_c}"
        if chave not in contribuintes_por_empfili:
            contribuintes_por_empfili[chave] = [("", "Nenhum contribuinte cadastrado nesta filial")]

    return (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        contribuintes_por_empfili,
    )


def _carregar_choices_empresas(db_alias, banco):
    (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        contribuintes_por_empfili,
    ) = _montar_mapas_dinamicos(db_alias, banco)
    return (
        choices_empresa_combo,
        empr_padrao_cod,
        fili_padrao_cod,
        contribuintes_por_empfili,
    )


def _carregar_choices_contribuintes(contribuintes_por_empfili, empr, fili):
    if not empr or not fili:
        return [("", "Selecione a empresa e a filial primeiro...")]
    chave = f"{int(empr)}_{int(fili)}"
    return contribuintes_por_empfili.get(chave, [("", "Selecione...")])


class DependentescontrCreateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentescontr/form.html"
    form_class = DependentescontrForm

    def get_initial(self):
        initial = super().get_initial()
        (
            _,
            empr_padrao_cod,
            fili_padrao_cod,
            _,
        ) = _obter_empresa_padrao_e_filiais(self.request.db_alias, self.request.banco)

        initial_empresa_url = self.request.GET.get("empr") or self.request.GET.get("empresa")
        initial_filial_url = self.request.GET.get("fili") or self.request.GET.get("filial")
        initial_contribuinte = self.request.GET.get("contr") or self.request.GET.get("contribuinte")

        filial_inicial = int(initial_filial_url) if initial_filial_url and str(initial_filial_url).isdigit() else fili_padrao_cod

        initial["depecontr_empr"] = filial_inicial
        initial["depecontr_fili"] = filial_inicial
        initial["depecontr_contr"] = initial_contribuinte
        initial["depecontr_invalido"] = False
        initial["depecontr_dependente_irrf"] = False
        initial["depecontr_dependente_salario_familia"] = False
        initial["_empr_padrao_cod"] = empr_padrao_cod
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        initial_fili_do_combo = form.initial.get("depecontr_empr") or self.request.GET.get("fili") or 1
        initial_fili_input = form.initial.get("depecontr_fili") or self.request.GET.get("fili") or 1
        filial_real = initial_fili_do_combo if initial_fili_do_combo else initial_fili_input
        initial_contribuinte = form.initial.get("depecontr_contr") or self.request.GET.get("contr") or self.request.GET.get("contribuinte")
        banco_limpo = _digits_only(self.request.banco)

        (
            choices_empresa_combo,
            empr_padrao_cod,
            fili_padrao_cod,
            contribuintes_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        self._contribuintes_por_empfili_json = contribuintes_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        form.fields["depecontr_empr"].choices = choices_empresa_combo
        form.initial["depecontr_empr"] = filial_real
        form.initial["depecontr_fili"] = filial_real
        form.fields["depecontr_fili"].initial = filial_real

        choices_contr = _carregar_choices_contribuintes(
            contribuintes_por_empfili, empr_padrao_cod, filial_real
        )
        form.fields["depecontr_contr"].choices = choices_contr

        if initial_contribuinte:
            proximo_codigo = DependentescontrChaveService.proximo_codigo(
                banco=banco_limpo,
                db_alias=self.request.db_alias,
                empresa=empr_padrao_cod,
                filial=filial_real,
                contribuinte=initial_contribuinte,
            )
            form.initial["depecontr_codi"] = proximo_codigo
            form.fields["depecontr_codi"].initial = proximo_codigo

        return form

    def form_valid(self, form):
        banco_limpo = _digits_only(self.request.banco)
        (
            _,
            empr_padrao_cod,
            _,
            _,
        ) = _obter_empresa_padrao_e_filiais(self.request.db_alias, banco_limpo)
        dados = form.cleaned_data.copy()
        dados["registro"] = banco_limpo

        filial_escolhida = (
            (dados.get("depecontr_empr") if str(dados.get("depecontr_empr") or "").isdigit() else None)
            or (dados.get("depecontr_fili") if str(dados.get("depecontr_fili") or "").isdigit() else None)
            or form.initial.get("depecontr_empr")
            or self.request.GET.get("fili")
            or 1
        )
        filial_escolhida = int(filial_escolhida)

        escolha_contribuinte = dados.get("depecontr_contr") or form.initial.get("depecontr_contr") or self.request.GET.get("contr") or self.request.GET.get("contribuinte")
        dados["depecontr_empr"] = empr_padrao_cod
        dados["depecontr_fili"] = filial_escolhida
        dados["depecontr_contr"] = escolha_contribuinte

        if not dados.get("depecontr_codi") and escolha_contribuinte:
            dados["depecontr_codi"] = DependentescontrChaveService.proximo_codigo(
                banco=banco_limpo,
                db_alias=self.request.db_alias,
                empresa=empr_padrao_cod,
                filial=filial_escolhida,
                contribuinte=escolha_contribuinte,
            )

        self._sucesso_empr = empr_padrao_cod
        self._sucesso_fili = filial_escolhida
        self._sucesso_contr = escolha_contribuinte

        DependentescontrCriarService.criar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente de contribuinte criado com sucesso.")
        return redirect(self.get_success_url())

    def _base_sucesso_url(self):
        banco_limpo = _digits_only(self.request.banco)
        empr = getattr(self, "_sucesso_empr", None) or self.request.GET.get("empr") or self.request.GET.get("empresa") or 1
        fili = getattr(self, "_sucesso_fili", None) or self.request.GET.get("fili") or self.request.GET.get("filial") or 1
        contr = getattr(self, "_sucesso_contr", None) or self.request.GET.get("contr") or self.request.GET.get("contribuinte")
        if contr and empr and fili:
            try:
                return (
                    reverse(
                        "contribuintes:atualizar",
                        kwargs={"empr": int(empr), "fili": int(fili), "codi": int(contr)},
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("contribuintes:listar") + f"?banco={banco_limpo}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        banco_limpo = _digits_only(self.request.banco)
        if not hasattr(self, "_contribuintes_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                contribuintes_json,
            ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        else:
            contribuintes_json = self._contribuintes_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        import json
        ctx["contribuintes_por_empfili_json"] = json.dumps(contribuintes_json)
        ctx["empr_padrao_cod"] = empr_padrao_cod
        empr = self.request.GET.get("empr") or self.request.GET.get("empresa") or empr_padrao_cod
        fili = self.request.GET.get("fili") or self.request.GET.get("filial") or 1
        contr = self.request.GET.get("contr") or self.request.GET.get("contribuinte")
        ctx["modo_edicao"] = False
        ctx["mostrar_cabecalho"] = True
        ctx["contribuinte_contexto"] = _obter_contexto_contribuinte(self.request, empr, fili, contr)
        ctx["url_voltar"] = self._base_sucesso_url()

        cidades_lista = []
        for codigo, nome, uf in _TOP_CIDADES_IBGE:
            try:
                codigo_num = int(codigo)
            except Exception:
                continue
            cidades_lista.append(
                {
                    "codigo_str": f"{codigo:0>7}",
                    "codigo_num": codigo_num,
                    "nome": nome,
                    "uf": uf,
                    "label": f"{codigo:0>7} — {nome} / {uf}",
                }
            )
        ctx["cidades_lista"] = cidades_lista

        return ctx
