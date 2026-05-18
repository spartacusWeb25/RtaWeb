# Recuperação de tabela PostgreSQL via Docker + Backup `.dump`

## Cenário

Recuperar dados apagados da tabela `folhamensal` usando:

* Docker
* PostgreSQL 16
* backup automático `.dump`
* restore temporário
* reimportação para banco principal

---

# 1. Verificar containers PostgreSQL

No host Ubuntu:

```bash
docker ps
```

Exemplo:

```bash
CONTAINER ID   IMAGE         NAMES
93ae7fcb20ca   postgres:16   postgres16_migrado
ff80ac358717   postgres:16   postgres16_backup
```

---

# 2. Localizar backups automáticos

No host:

```bash
find /home/ubuntu -iname "*.dump"
```

Exemplo:

```bash
/home/ubuntu/apps/RtaWeb/migracao_postgres/backups/rtaweb0001_pg16_auto_2026-05-18_08-08-17.dump
```

---

# 3. Criar banco temporário de restore

Entrar no container PostgreSQL:

```bash
docker exec -it postgres16_migrado bash
```

Criar banco temporário:

```bash
createdb -U postgres restore_tmp
```

Sair:

```bash
exit
```

---

# 4. Copiar backup para dentro do container

No host Ubuntu:

```bash
docker cp /home/ubuntu/apps/RtaWeb/migracao_postgres/backups/rtaweb0001_pg16_auto_2026-05-18_08-08-17.dump postgres16_migrado:/tmp/backup.dump
```

---

# 5. Restaurar backup no banco temporário

No host Ubuntu:

```bash
docker exec -i postgres16_migrado pg_restore -U postgres -d restore_tmp /tmp/backup.dump
```

---

# 6. Confirmar restore

Entrar no PostgreSQL:

```bash
docker exec -it postgres16_migrado psql -U postgres -d restore_tmp
```

Consultar dados:

```sql
SELECT COUNT(*)
FROM folhamensal
WHERE registro = '22553164000189';
```

Consultar registros:

```sql
SELECT *
FROM folhamensal
WHERE registro = '22553164000189'
LIMIT 10;
```

Sair:

```sql
\q
```

---

# 7. Verificar banco principal

Listar bancos:

```bash
docker exec -it postgres16_migrado psql -U postgres -c "\l"
```

Exemplo:

```txt
rtaweb0001
restore_tmp
```

Banco real:

```txt
rtaweb0001
```

---

# 8. Exportar dados restaurados para CSV

No host Ubuntu:

```bash
docker exec -i postgres16_migrado psql -U postgres -d restore_tmp -c "\copy (
    SELECT *
    FROM folhamensal
    WHERE registro = '22553164000189'
) TO '/tmp/folhamensal_restore.csv' WITH CSV HEADER"
```

---

# 9. Importar dados no banco principal

No host Ubuntu:

```bash
docker exec -i postgres16_migrado psql -U postgres -d rtaweb0001 -c "\copy folhamensal FROM '/tmp/folhamensal_restore.csv' WITH CSV HEADER"
```

---

# 10. Confirmar recuperação

Entrar no banco real:

```bash
docker exec -it postgres16_migrado psql -U postgres -d rtaweb0001
```

Consultar:

```sql
SELECT COUNT(*)
FROM folhamensal
WHERE registro = '22553164000189';
```

---

# 11. Problema que causou o delete em massa

Tabela legado com chave composta:

```txt
registro
fome_empr
fome_fili
fome_func
fome_refe
fome_even
```

Mas o model Django estava com:

```python
primary_key=True
```

somente em:

```python
registro
```

Então:

```python
instance.delete()
```

gerou:

```sql
DELETE FROM folhamensal
WHERE registro = '22553164000189'
```

apagando vários registros.

---

# 12. Regra para tabelas legado sem PK real

NUNCA usar:

```python
instance.save()
instance.delete()
```

Usar SEMPRE:

```python
.queryset.filter(...).update(...)
.queryset.filter(...).delete()
```

com chave composta completa.

---

# 13. Padrão seguro para delete

```python
Folhamensal.objects.using(db_alias).filter(
    registro=banco,
    fome_empr=fome_empr,
    fome_fili=fome_fili,
    fome_func=fome_func,
    fome_refe=fome_refe,
    fome_even=fome_even,
).delete()
```

---

# 14. Padrão seguro para update

```python
Folhamensal.objects.using(db_alias).filter(
    registro=banco,
    fome_empr=fome_empr,
    fome_fili=fome_fili,
    fome_func=fome_func,
    fome_refe=fome_refe,
    fome_even=fome_even,
).update(
    fome_valo=novo_valor
)
```

---

# 15. Nunca esquecer

* `docker` roda no HOST
* dentro do container NÃO existe comando `docker`
* restore sempre em banco temporário
* nunca restaurar dump diretamente sobre produção
* tabela legado sem PK real precisa de tratamento manual
