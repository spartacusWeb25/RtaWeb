from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from dependentesrh.web.forms import DependentesrhForm
from dependentesrh.services.criar import DependentesCriarService
from dependentesrh.services.chave import DependentesChaveService
from dependentesrh.web.choices import _TOP_CIDADES_IBGE
from funcionarios.services.logic import FuncionariosService
from empresas.models import Empresas


def _obter_contexto_funcionario(request, empresa, filial, funcionario):
    if not empresa or not filial or not funcionario:
        return None
    try:
        from funcionarios.models import Funcionarios
        from empresas.models import Empresas

        dados = {
            "funcionario": None,
            "empresa_nome": "",
            "empresa": empresa,
            "filial": filial,
            "empresa_display": "",
            "filial_display": "",
            "funcionario_display": "",
        }

        emp = (
            Empresas.objects.using(request.db_alias)
            .filter(registro=request.banco, empr_empr=int(empresa), empr_fili=1)
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
            .filter(registro=request.banco, empr_empr=int(empresa), empr_fili=int(filial))
            .values("empr_nome")
            .first()
        )
        if fil:
            dados["filial_display"] = f"{filial} — {fil['empr_nome']}"
        else:
            dados["filial_display"] = str(filial)

        func = (
            Funcionarios.objects.using(request.db_alias)
            .filter(
                registro=request.banco,
                func_empr=int(empresa),
                func_fili=int(filial),
                func_codi=int(funcionario),
            )
            .values("func_codi", "func_nome", "func_cargo", "func_empr", "func_fili", "func_admissao", "func_cpf")
            .first()
        )
        if func:
            dados["funcionario"] = func
            dados["funcionario_display"] = str(func["func_codi"])
        else:
            dados["funcionario_display"] = str(funcionario)

        return dados
    except Exception:
        return None


def _obter_empresa_padrao_e_filiais(db_alias, banco):
    empresa_padrao = None
    try:
        empresa_padrao = FuncionariosService.obter_empresa_padrao(
            banco=banco, db_alias=db_alias
        )
    except Exception:
        empresa_padrao = None
    empr_padrao_cod = int(getattr(empresa_padrao, "empr_empr", 1) or 1)
    fili_padrao_cod = int(getattr(empresa_padrao, "empr_fili", 1) or 1)

    linhas_filiais = []
    try:
        qs = (
            Empresas.objects.using(db_alias)
            .filter(registro=banco)
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

    funcionarios_por_empfili = {}
    try:
        funcionarios = FuncionariosService.listar_por_banco(banco=banco) or []
        for func in funcionarios:
            try:
                fempr = int(getattr(func, "func_empr", 0) or 0)
                ffili = int(getattr(func, "func_fili", 0) or 0)
                codf = int(getattr(func, "func_codi", 0) or 0)
                nomef = getattr(func, "func_nome", "") or "Sem nome"
            except Exception:
                continue
            if not fempr or not ffili or not codf:
                continue
            chave = f"{fempr}_{ffili}"
            if chave not in funcionarios_por_empfili:
                funcionarios_por_empfili[chave] = []
            funcionarios_por_empfili[chave].append((str(codf), f"{codf} — {nomef}"))
    except Exception:
        pass

    for chave, lista in funcionarios_por_empfili.items():
        lista.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        funcionarios_por_empfili[chave] = [("", "Selecione...")] + lista
    for (empr_c, fili_c, _) in filiais_da_empresa_logada:
        chave = f"{empr_c}_{fili_c}"
        if chave not in funcionarios_por_empfili:
            funcionarios_por_empfili[chave] = [("", "Nenhum funcionário cadastrado nesta filial")]

    return (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        funcionarios_por_empfili,
    )


def _carregar_choices_empresas(db_alias, banco):
    (
        empr_padrao_cod,
        fili_padrao_cod,
        choices_empresa_combo,
        funcionarios_por_empfili,
    ) = _montar_mapas_dinamicos(db_alias, banco)
    return (
        choices_empresa_combo,
        empr_padrao_cod,
        fili_padrao_cod,
        funcionarios_por_empfili,
    )


def _carregar_choices_funcionarios(funcionarios_por_empfili, empr, fili):
    if not empr or not fili:
        return [("", "Selecione a empresa e a filial primeiro...")]
    chave = f"{int(empr)}_{int(fili)}"
    return funcionarios_por_empfili.get(chave, [("", "Selecione...")])


class DependentesCreateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentesrh/form.html"
    form_class = DependentesrhForm

    def get_initial(self):
        initial = super().get_initial()
        (
            _,
            empr_padrao_cod,
            fili_padrao_cod,
            _,
        ) = _obter_empresa_padrao_e_filiais(self.request.db_alias, self.request.banco)

        initial_empresa_url = self.request.GET.get("empresa")
        initial_filial_url = self.request.GET.get("filial")
        initial_funcionario = self.request.GET.get("funcionario")

        filial_inicial = int(initial_filial_url) if initial_filial_url and str(initial_filial_url).isdigit() else fili_padrao_cod

        initial["depe_empr"] = filial_inicial
        initial["depe_fili"] = filial_inicial
        initial["depe_func"] = initial_funcionario
        initial["depe_invalido"] = False
        initial["_empr_padrao_cod"] = empr_padrao_cod
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        initial_fili_do_combo = form.initial.get("depe_empr") or self.request.GET.get("filial") or 1
        initial_fili_input = form.initial.get("depe_fili") or self.request.GET.get("filial") or 1
        filial_real = initial_fili_do_combo if initial_fili_do_combo else initial_fili_input
        initial_funcionario = form.initial.get("depe_func") or self.request.GET.get("funcionario")

        (
            choices_empresa_combo,
            empr_padrao_cod,
            fili_padrao_cod,
            funcionarios_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, self.request.banco)
        self._funcionarios_por_empfili_json = funcionarios_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        form.fields["depe_empr"].choices = choices_empresa_combo
        form.initial["depe_empr"] = filial_real
        form.initial["depe_fili"] = filial_real
        form.fields["depe_fili"].initial = filial_real

        choices_func = _carregar_choices_funcionarios(
            funcionarios_por_empfili, empr_padrao_cod, filial_real
        )
        form.fields["depe_func"].choices = choices_func

        if initial_funcionario:
            proximo_codigo = DependentesChaveService.proximo_codigo(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                empresa=empr_padrao_cod,
                filial=filial_real,
                funcionario=initial_funcionario,
            )
            form.initial["depe_codi"] = proximo_codigo
            form.fields["depe_codi"].initial = proximo_codigo

        return form

    def form_valid(self, form):
        (
            _,
            empr_padrao_cod,
            _,
            _,
        ) = _obter_empresa_padrao_e_filiais(self.request.db_alias, self.request.banco)
        dados = form.cleaned_data.copy()
        dados["registro"] = self.request.banco

        filial_escolhida = (
            (dados.get("depe_empr") if str(dados.get("depe_empr") or "").isdigit() else None)
            or (dados.get("depe_fili") if str(dados.get("depe_fili") or "").isdigit() else None)
            or form.initial.get("depe_empr")
            or self.request.GET.get("filial")
            or 1
        )
        filial_escolhida = int(filial_escolhida)

        escolha_funcionario = dados.get("depe_func") or form.initial.get("depe_func") or self.request.GET.get("funcionario")
        dados["depe_empr"] = empr_padrao_cod
        dados["depe_fili"] = filial_escolhida
        dados["depe_func"] = escolha_funcionario

        if not dados.get("depe_codi") and escolha_funcionario:
            dados["depe_codi"] = DependentesChaveService.proximo_codigo(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                empresa=empr_padrao_cod,
                filial=filial_escolhida,
                funcionario=escolha_funcionario,
            )

        self._sucesso_empr = empr_padrao_cod
        self._sucesso_fili = filial_escolhida
        self._sucesso_func = escolha_funcionario

        DependentesCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente criado com sucesso.")
        return redirect(self.get_success_url())

    def _base_sucesso_url(self):
        empr = getattr(self, "_sucesso_empr", None) or self.request.GET.get("empresa") or 1
        fili = getattr(self, "_sucesso_fili", None) or self.request.GET.get("filial") or 1
        func = getattr(self, "_sucesso_func", None) or self.request.GET.get("funcionario")
        if func and empr and fili:
            try:
                return (
                    reverse(
                        "funcionarios:atualizar",
                        kwargs={"func_empr": int(empr), "func_fili": int(fili), "func_codi": int(func)},
                    )
                    + f"?banco={self.request.banco}#tab-parentes"
                )
            except Exception:
                pass
        return reverse("dependentesrh:listar") + f"?banco={self.request.banco}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not hasattr(self, "_funcionarios_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                funcionarios_json,
            ) = _carregar_choices_empresas(self.request.db_alias, self.request.banco)
        else:
            funcionarios_json = self._funcionarios_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        import json
        ctx["funcionarios_por_empfili_json"] = json.dumps(funcionarios_json)
        ctx["empr_padrao_cod"] = empr_padrao_cod
        empr = self.request.GET.get("empresa") or empr_padrao_cod
        fili = self.request.GET.get("filial") or 1
        func = self.request.GET.get("funcionario")
        ctx["modo_edicao"] = False
        ctx["mostrar_cabecalho"] = True
        ctx["funcionario_contexto"] = _obter_contexto_funcionario(self.request, empr, fili, func)
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
