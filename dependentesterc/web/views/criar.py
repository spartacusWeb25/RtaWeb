from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
import json

from core.mixin import BancoObrigatorioMixin
from dependentesterc.web.forms import DependentestercForm
from dependentesterc.services.criar import DependentestercCriarService
from dependentesterc.services.chave import DependentestercChaveService
from empresas.models import Empresas
from terceiros.web.choices import CIDADES_POR_CODIGO


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _buscar_terceiros_por_empfili(db_alias, banco):
    banco_limpo = _digits_only(banco)
    terceiros_por_empfili = {}
    try:
        try:
            from terceiros.models import Terceiros
            from terceiros.services.listar import ListarTerceirosService
            try:
                terceiros = ListarTerceirosService.listar(
                    banco=banco_limpo,
                    db_alias=db_alias,
                ) or []
            except Exception:
                terceiros = (
                    Terceiros.objects.using(db_alias)
                    .filter(registro=banco_limpo)
                    .all()
                )
        except Exception:
            terceiros = []
        for terc_obj in list(terceiros):
            try:
                tempr = int(getattr(terc_obj, "terc_empr", 0) or 0)
                tfili = int(getattr(terc_obj, "terc_fili", 0) or 0)
                codt = int(getattr(terc_obj, "terc_codi", 0) or 0)
                nomet = getattr(terc_obj, "terc_nome", "") or "Sem nome"
            except Exception:
                continue
            if not tempr or not tfili or not codt:
                continue
            chave = f"{tempr}_{tfili}"
            if chave not in terceiros_por_empfili:
                terceiros_por_empfili[chave] = []
            terceiros_por_empfili[chave].append((str(codt), f"{codt} — {nomet}"))
    except Exception:
        pass

    for chave, lista in terceiros_por_empfili.items():
        lista.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        terceiros_por_empfili[chave] = [("", "Selecione...")] + lista
    return terceiros_por_empfili


def _obter_contexto_terceiro(request, empresa, filial, terceiro):
    if not empresa or not filial or not terceiro:
        return None
    try:
        banco_limpo = _digits_only(request.banco)

        dados = {
            "terceiro": None,
            "empresa_nome": "",
            "empresa": empresa,
            "filial": filial,
            "empresa_display": "",
            "filial_display": "",
            "terceiro_display": "",
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

        try:
            from terceiros.models import Terceiros
            terc = (
                Terceiros.objects.using(request.db_alias)
                .filter(
                    registro=banco_limpo,
                    terc_empr=int(empresa),
                    terc_fili=int(filial),
                    terc_codi=int(terceiro),
                )
                .values("terc_codi", "terc_nome", "terc_cpf", "terc_empr", "terc_fili")
                .first()
            )
            if terc:
                dados["terceiro"] = terc
                dados["terceiro_display"] = str(terc["terc_codi"])
            else:
                dados["terceiro_display"] = str(terceiro)
        except Exception:
            dados["terceiro_display"] = str(terceiro)

        return dados
    except Exception:
        return None


def _obter_empresa_padrao_e_filiais(db_alias, banco):
    banco_limpo = _digits_only(banco)
    empresa_padrao = None
    empr_padrao_cod = 1
    fili_padrao_cod = 1

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

    terceiros_por_empfili = _buscar_terceiros_por_empfili(db_alias, banco)

    for (empr_c, fili_c, _) in filiais_da_empresa_logada:
        chave = f"{empr_c}_{fili_c}"
        if chave not in terceiros_por_empfili:
            terceiros_por_empfili[chave] = [("", "Nenhum terceiro cadastrado nesta filial")]

    return (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        terceiros_por_empfili,
    )


def _carregar_choices_empresas(db_alias, banco):
    (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        terceiros_por_empfili,
    ) = _montar_mapas_dinamicos(db_alias, banco)
    return (
        choices_empresa_combo,
        empr_padrao_cod,
        fili_padrao_cod,
        terceiros_por_empfili,
    )


def _carregar_choices_terceiros(terceiros_por_empfili, empr, fili):
    if not empr or not fili:
        return [("", "Selecione a empresa e a filial primeiro...")]
    chave = f"{int(empr)}_{int(fili)}"
    return terceiros_por_empfili.get(chave, [("", "Selecione...")])


class DependentestercCreateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentesterc/form.html"
    form_class = DependentestercForm

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
        initial_terceiro = self.request.GET.get("terc") or self.request.GET.get("terceiro")

        empr_inicial = int(initial_empresa_url) if initial_empresa_url and str(initial_empresa_url).isdigit() else empr_padrao_cod
        fili_inicial = int(initial_filial_url) if initial_filial_url and str(initial_filial_url).isdigit() else fili_padrao_cod
        terc_inicial = int(initial_terceiro) if initial_terceiro and str(initial_terceiro).isdigit() else None

        # --- GARANTIA TOTAL de que TODAS as chaves de PK composta existem no initial
        #     (evita KeyError no template ao re-renderizar com erros de validação) ---
        initial["registro"] = _digits_only(self.request.banco)
        initial["depe_empr"] = empr_inicial
        initial["depe_fili"] = fili_inicial
        initial["depe_terc"] = terc_inicial
        initial["depe_codi"] = None  # Garante existência da chave (não causa KeyError)
        initial["depe_invalido"] = False
        initial["_empr_padrao_cod"] = empr_padrao_cod
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        banco_limpo = _digits_only(self.request.banco)

        (
            _,
            empr_padrao_cod,
            fili_padrao_cod,
            terceiros_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        self._terceiros_por_empfili_json = terceiros_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        # --- Resolver valores de PK composta (ordem: form initial → GET URL → padrão) ---
        empr_val = (
            form.initial.get("depe_empr")
            or self.request.GET.get("empr") or self.request.GET.get("empresa")
            or empr_padrao_cod
        )
        fili_val = (
            form.initial.get("depe_fili")
            or self.request.GET.get("fili") or self.request.GET.get("filial")
            or fili_padrao_cod
        )
        terc_val = (
            form.initial.get("depe_terc")
            or self.request.GET.get("terc") or self.request.GET.get("terceiro")
            or None
        )

        empr_val = int(empr_val) if str(empr_val or "").isdigit() else empr_padrao_cod
        fili_val = int(fili_val) if str(fili_val or "").isdigit() else fili_padrao_cod
        terc_val = int(terc_val) if str(terc_val or "").isdigit() else None

        # --- Garantir que initials estão corretos nos campos hidden ---
        form.initial["depe_empr"] = empr_val
        form.initial["depe_fili"] = fili_val
        form.initial["depe_terc"] = terc_val
        form.initial["registro"] = banco_limpo

        # --- Pré-calcula o próximo código do dependente (se tivermos todos os pais) ---
        if terc_val:
            proximo_codigo = DependentestercChaveService.proximo_codigo(
                banco=banco_limpo,
                db_alias=self.request.db_alias,
                empresa=empr_val,
                filial=fili_val,
                terceiro=terc_val,
            )
            form.initial["depe_codi"] = proximo_codigo

        self._resolvido_empr = empr_val
        self._resolvido_fili = fili_val
        self._resolvido_terc = terc_val

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

        # --- REGRA DependentesRH (Funcionarios): SEMPRE usa empresa LOGADA = empr_padrao_cod
        #     (NÃO confia em campos hidden do formulario - segurança e consistencia) ---
        dados["registro"] = banco_limpo

        # --- FILIAL: cadeia de fallback (hidden depe_empr/depe_fili → initial → GET URL → padrão 1)
        filial_escolhida = (
            (dados.get("depe_empr") if str(dados.get("depe_empr") or "").isdigit() else None)
            or (dados.get("depe_fili") if str(dados.get("depe_fili") or "").isdigit() else None)
            or form.initial.get("depe_fili")
            or form.initial.get("depe_empr")
            or self.request.GET.get("fili")
            or self.request.GET.get("filial")
            or 1
        )
        filial_escolhida = int(filial_escolhida)

        # --- TERCEIRO: cadeia de fallback (dados hidden → initial → GET URL)
        escolha_terceiro = (
            dados.get("depe_terc")
            or form.initial.get("depe_terc")
            or self.request.GET.get("terc")
            or self.request.GET.get("terceiro")
        )

        # --- VALIDACAO CRITICA: nao grava se nao informou terceiro
        if not escolha_terceiro or not str(escolha_terceiro or "").isdigit() or int(escolha_terceiro) <= 0:
            messages.error(
                self.request,
                "Erro ao criar dependente: nao foi informado o Terceiro (verifique se esta tela foi aberta a partir do botao 'Novo Dependente' na aba Dependentes do Terceiro)."
            )
            return redirect(self._base_sucesso_url())

        # --- GRAVA: empresa = empr_padrao_cod (empresa LOGADA da licenca), filial e terceiro calculados ---
        dados["depe_empr"] = empr_padrao_cod
        dados["depe_fili"] = filial_escolhida
        dados["depe_terc"] = int(escolha_terceiro)

        # --- PROXIMO CODIGO: sempre via service (usa a chave composta real)
        if not dados.get("depe_codi") or not str(dados["depe_codi"] or "").isdigit():
            dados["depe_codi"] = DependentestercChaveService.proximo_codigo(
                banco=banco_limpo,
                db_alias=self.request.db_alias,
                empresa=empr_padrao_cod,
                filial=filial_escolhida,
                terceiro=int(escolha_terceiro),
            )

        self._sucesso_empr = empr_padrao_cod
        self._sucesso_fili = filial_escolhida
        self._sucesso_terc = int(escolha_terceiro)

        DependentestercCriarService.criar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente de terceiro criado com sucesso.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("=" * 70)
        print("[DEBUG DepTerc CRIAR form_invalid] form.errors =")
        for k, v in (form.errors or {}).items():
            print(f"  - Campo '{k}': {v}")
        print("[DEBUG DepTerc CRIAR form_invalid] cleaned_data (se existir):")
        try:
            for k, v in (form.cleaned_data or {}).items():
                print(f"  - {k} = {repr(v)[:80]}")
        except Exception:
            pass
        print("=" * 70)
        return super().form_invalid(form)

    def _base_sucesso_url(self):
        banco_limpo = _digits_only(self.request.banco)
        empr = getattr(self, "_sucesso_empr", None) or self.request.GET.get("empr") or self.request.GET.get("empresa") or 1
        fili = getattr(self, "_sucesso_fili", None) or self.request.GET.get("fili") or self.request.GET.get("filial") or 1
        terc = getattr(self, "_sucesso_terc", None) or self.request.GET.get("terc") or self.request.GET.get("terceiro")
        if terc and empr and fili:
            try:
                return (
                    reverse(
                        "terceiros:atualizar",
                        kwargs={"empr": int(empr), "fili": int(fili), "codi": int(terc)},
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("terceiros:listar") + f"?banco={banco_limpo}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        banco_limpo = _digits_only(self.request.banco)
        if not hasattr(self, "_terceiros_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                terceiros_json,
            ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        else:
            terceiros_json = self._terceiros_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        import json
        ctx["terceiros_por_empfili_json"] = json.dumps(terceiros_json)
        ctx["empr_padrao_cod"] = empr_padrao_cod
        empr = getattr(self, "_resolvido_empr", None) or self.request.GET.get("empr") or self.request.GET.get("empresa") or empr_padrao_cod
        fili = getattr(self, "_resolvido_fili", None) or self.request.GET.get("fili") or self.request.GET.get("filial") or 1
        terc = getattr(self, "_resolvido_terc", None) or self.request.GET.get("terc") or self.request.GET.get("terceiro")

        # --- Garante o valor do código do dependente para exibir no input ---
        if terc and str(terc or "").isdigit():
            try:
                empr_i = int(empr)
                fili_i = int(fili)
                terc_i = int(terc)
                ctx["proximo_codigo_dep"] = DependentestercChaveService.proximo_codigo(
                    banco=banco_limpo,
                    db_alias=self.request.db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                    terceiro=terc_i,
                )
            except Exception:
                ctx["proximo_codigo_dep"] = 1

        ctx["modo_edicao"] = False
        ctx["mostrar_cabecalho"] = True
        ctx["terceiro_contexto"] = _obter_contexto_terceiro(self.request, empr, fili, terc)
        ctx["url_voltar"] = self._base_sucesso_url()
        ctx["cidades_por_codigo_json"] = mark_safe(
            json.dumps(CIDADES_POR_CODIGO, ensure_ascii=False)
        )

        return ctx
