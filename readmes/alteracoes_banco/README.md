# Alteracoes de Banco

Esta pasta guarda scripts SQL versionados para alteracoes de estrutura e apoio ao deploy.

## Padrao de Nome

Use o formato abaixo para os arquivos:

```text
AAAA-MM-DD_descricao_curta.sql
```

Exemplos:

```text
2026-06-22_tabelas_inss_irrf.sql
2026-06-23_usuarios_licencas.sql
```

## Regras Recomendadas

- Criar um arquivo por alteracao logica.
- Preferir scripts nao destrutivos.
- Documentar no topo do arquivo o objetivo e as tabelas afetadas.
- Informar se existe impacto em dados antigos.
- Incluir uma consulta de validacao ao final do script, quando fizer sentido.

## Ordem de Execucao

Para publicacao:

1. Fazer backup do banco.
2. Executar o script SQL no ambiente.
3. Validar se as colunas, tabelas ou indices foram criados corretamente.
4. Publicar o codigo da aplicacao.
5. Testar o fluxo funcional relacionado a alteracao.

## Observacoes

- Para tabelas legadas com `managed = False`, nao depender apenas de migrations Django.
- Sempre versionar o SQL correspondente junto com o ajuste de codigo.
- Se houver necessidade de popular valores iniciais, fazer isso em script separado ou documentado no mesmo arquivo.
