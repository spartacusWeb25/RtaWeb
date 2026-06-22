from tabelainss.services.chave import TabelaInssChaveService


class TabelaInssEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        tabelainss = TabelaInssChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not tabelainss:
            raise ValueError("Tabela INSS não encontrado.")

        tabela = dados.get("tabe_refe")
        if tabelainss and tabela != tabelainss.tabe_refe:
            raise ValueError("Não é permitido alterar a referência (tabe_refe).")

        for campo in (
            "tabe_fa01",
            "tabe_pe01",
            "tabe_fa02",
            "tabe_pe02",
            "tabe_fa03",
            "tabe_pe03",
            "tabe_fa04",
            "tabe_pe04",
            "tabe_mini_gps",
        ):
            if campo in dados:
                setattr(tabelainss, campo, dados.get(campo))

        tabelainss.save(using=db_alias)

        return tabelainss
