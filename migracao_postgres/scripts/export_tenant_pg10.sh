#!/bin/bash

set -e

DB_HOST="${DB_HOST:-base.rtalmeida.com.br}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-rtaweb0001}"
DB_NAME="${DB_NAME:-rtaweb0001}"
CNPJ="$1"

if [ -z "$CNPJ" ]; then
  echo "Uso: ./export_tenant_pg10.sh 22553164000189"
  exit 1
fi

DATA=$(date +"%Y-%m-%d_%H-%M-%S")
OUT_DIR="./backups"
OUT_FILE="$OUT_DIR/tenant_${CNPJ}_${DATA}.sql"

mkdir -p "$OUT_DIR"

echo "-- Dump filtrado do tenant $CNPJ" > "$OUT_FILE"
echo "BEGIN;" >> "$OUT_FILE"

TABLES=$(psql \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -Atc "
    SELECT table_schema || '.' || table_name
    FROM information_schema.columns
    WHERE column_name = 'registro'
      AND table_schema = 'public'
    GROUP BY table_schema, table_name
    ORDER BY table_name;
  "
)

for TABLE in $TABLES; do
  echo "Exportando $TABLE..."

  echo "" >> "$OUT_FILE"
  echo "-- Tabela $TABLE" >> "$OUT_FILE"

  pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --data-only \
    --column-inserts \
    --table="$TABLE" \
    --where="registro = '$CNPJ'" \
    >> "$OUT_FILE"
done

echo "COMMIT;" >> "$OUT_FILE"

echo "Dump criado em: $OUT_FILE"