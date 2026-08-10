from empresas.models import Empresas


class AdmissaoPreliminarService:
    SESSION_KEY = "admissao_preliminar_prefill_funcionario"

    @staticmethod
    def buscar_empresa(*, banco, db_alias, codigo_empresa=None):
        qs = Empresas.objects.using(db_alias).filter(registro=banco).order_by("empr_fili", "empr_nome")
        if codigo_empresa:
            qs = qs.filter(empr_empr=codigo_empresa)
        return qs.first()

    @classmethod
    def obter_nome_empresa(cls, *, banco, db_alias, codigo_empresa=None):
        empresa = cls.buscar_empresa(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
        )
        return getattr(empresa, "empr_nome", "") or ""

    @classmethod
    def obter_codigo_empresa_inicial(cls, *, banco, db_alias):
        empresa = cls.buscar_empresa(banco=banco, db_alias=db_alias)
        return getattr(empresa, "empr_empr", None)

    @classmethod
    def consultar_esocial(cls, *, banco, db_alias, dados):
        empresa = cls.buscar_empresa(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=dados.get("empresa"),
        )
        if not empresa:
            return {
                "sucesso": False,
                "mensagem": "Informe uma empresa valida para consultar o eSocial.",
                "dados": {},
            }

        return {
            "sucesso": True,
            "mensagem": (
                "Integracao com o eSocial preparada, mas ainda nao configurada neste ambiente. "
                "Os dados permaneceram prontos para conferencia e envio ao cadastro de funcionarios."
            ),
            "dados": {},
        }

    @classmethod
    def montar_prefill_funcionario(cls, dados):
        def _serializar(valor):
            if valor in (None, ""):
                return None
            if hasattr(valor, "isoformat"):
                return valor.isoformat()
            if hasattr(valor, "__class__") and valor.__class__.__name__ == "Decimal":
                return format(valor, "f")
            if isinstance(valor, (list, tuple)):
                return [_serializar(v) for v in valor]
            if isinstance(valor, dict):
                return {k: _serializar(v) for k, v in valor.items()}
            return valor

        prefill = {
            "func_empr": dados.get("empresa") or "",
            "func_admissao_preliminar": dados.get("codigo") or "",
            "func_nome": dados.get("nome") or "",
            "func_nascimento": _serializar(dados.get("nascimento")) or "",
            "func_matricula_esocial": dados.get("matricula_esocial") or "",
            "func_cpf": dados.get("cpf") or "",
            "func_pis": dados.get("nis") or "",
            "func_admissao": _serializar(dados.get("admissao")) or "",
            "func_tipo_funcionario": dados.get("tipo_funcionario") or "",
            "func_salario_base": _serializar(dados.get("salario_base")) or "",
            "func_categoria_esocial": dados.get("categoria_esocial") or "",
            "func_vinculo_empregaticio": dados.get("vinculo_empregaticio") or "",
            "func_cargo": dados.get("cargo") or "",
            "func_cbo_cargo": dados.get("cbo") or "",
            "func_tipo_contrato_trabalho": dados.get("tipo_contrato") or "",
            "func_prazo_experiencia_dias": dados.get("prazo_experiencia_dias") or "",
            "func_fim_primeiro_prazo": _serializar(dados.get("fim_primeiro_prazo")) or "",
        }
        return {chave: valor for chave, valor in prefill.items() if valor not in ("", None)}

    @classmethod
    def salvar_prefill_na_sessao(cls, *, session, dados):
        session[cls.SESSION_KEY] = cls.montar_prefill_funcionario(dados)
        session.modified = True

    @classmethod
    def consumir_prefill_da_sessao(cls, *, session):
        dados = session.pop(cls.SESSION_KEY, None)
        if dados is not None:
            session.modified = True
        return dados or {}
