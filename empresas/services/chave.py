class EmpresasChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "empr_empr",
        "empr_fili",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "registro": dados.get("registro"),
            "empr_empr": dados.get("empr_empr"),
            "empr_fili": dados.get("empr_fili"),
        }

    @staticmethod
    def _valor_inteiro_positivo(valor):
        """Garante que um campo inteiro da chave seja > 0 (não 0, não negativo, não None/vazio)."""
        if valor is None or valor == "":
            return False
        try:
            v = int(valor)
        except (TypeError, ValueError):
            return False
        return v > 0

    @staticmethod
    def chave_preenchida(chave):
        """Chave preenchida E válida: registro não vazio; empr_empr e empr_fili > 0."""
        if not chave:
            return False
        registro = (chave.get("registro") or "").strip()
        if not registro:
            return False
        if not EmpresasChaveService._valor_inteiro_positivo(chave.get("empr_empr")):
            return False
        if not EmpresasChaveService._valor_inteiro_positivo(chave.get("empr_fili")):
            return False
        return True

    @staticmethod
    def chave_valida(chave):
        """
        Validação completa da chave composta.
        Retorna (True, "") quando válida, ou (False, mensagem_de_erro) quando inválida.
        """
        if not isinstance(chave, dict):
            return False, "Chave inválida (tipo)."
        registro = (chave.get("registro") or "").strip()
        if not registro:
            return False, "Informe o registro (CNPJ) da licença."
        if len(registro) > 14:
            return False, "O registro (CNPJ) não pode ultrapassar 14 dígitos."
        if not EmpresasChaveService._valor_inteiro_positivo(chave.get("empr_empr")):
            return False, "Informe o Código da empresa maior que zero."
        try:
            if int(chave["empr_empr"]) > 999999:
                return False, "O Código da empresa não pode ultrapassar 6 dígitos."
        except (TypeError, ValueError):
            return False, "Informe um número válido para Código."
        if not EmpresasChaveService._valor_inteiro_positivo(chave.get("empr_fili")):
            return False, "Informe a Filial maior que zero (não pode ser 0)."
        try:
            if int(chave["empr_fili"]) > 999999:
                return False, "A Filial não pode ultrapassar 6 dígitos."
        except (TypeError, ValueError):
            return False, "Informe um número válido para Filial."
        return True, ""

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from empresas.models import Empresas

        chave = EmpresasChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not EmpresasChaveService.chave_preenchida(chave):
            return False

        return Empresas.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from empresas.models import Empresas

        chave = EmpresasChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not EmpresasChaveService.chave_preenchida(chave):
            return None

        return Empresas.objects.using(db_alias).filter(**chave).first()

    @staticmethod
    def remover(*, banco, db_alias, dados):
        from empresas.models import Empresas

        chave = EmpresasChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not EmpresasChaveService.chave_preenchida(chave):
            return 0

        deleted_count, _ = Empresas.objects.using(db_alias).filter(**chave).delete()
        return deleted_count
