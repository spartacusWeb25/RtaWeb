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
    def chave_preenchida(chave):
        return all(valor is not None and valor != "" for valor in chave.values())

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

    
