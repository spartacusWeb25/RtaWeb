from tabelairrf.services.chave import TabelaIrrfChaveService


class TabelaIrrfEditarService:
    @staticmethod
    def editar(*, banco, db_alias, dados):
        tabelairrf = TabelaIrrfChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not tabelairrf:
            raise ValueError("Tabela IRRF não encontrada.")

        referencia = dados.get("irrf_refe")
        if tabelairrf and referencia != tabelairrf.irrf_refe:
            raise ValueError("Não é permitido alterar a referência (irrf_refe).")

        for campo in (
            "irrf_fa01",
            "irrf_pe01",
            "irrf_de01",
            "irrf_fa02",
            "irrf_pe02",
            "irrf_de02",
            "irrf_fa03",
            "irrf_pe03",
            "irrf_de03",
            "irrf_fa04",
            "irrf_pe04",
            "irrf_de04",
            "irrf_dede",
            "irrf_desc_mini",
            "irrf_desc_simp",
        ):
            if campo in dados:
                setattr(tabelairrf, campo, dados.get(campo))

        tabelairrf.save(using=db_alias)

        return tabelairrf
