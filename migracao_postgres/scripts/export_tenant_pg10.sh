#!/bin/bash

set -e

DB_HOST="${DB_HOST:-base.rtalmeida.com.br}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-rtaweb0001}"
DB_NAME="${DB_NAME:-rtaweb0001}"
CNPJ="$1"


if [ -z "$CNPJ" ]; then
  echo "Uso: ./scripts/export_tenant_pg10.sh 22553164000189"
  exit 1
fi

DATA=$(date +"%Y-%m-%d_%H-%M-%S")
OUT_DIR="./backups"
OUT_FILE="$OUT_DIR/tenant_${CNPJ}_${DATA}.sql"

mkdir -p "$OUT_DIR"

echo "-- Dump filtrado por registro = $CNPJ" > "$OUT_FILE"
echo "BEGIN;" >> "$OUT_FILE"

TABLES=$(psql \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -Atc "
    SELECT table_schema || '|' || table_name
    FROM information_schema.columns
    WHERE column_name = 'registro'
      AND table_schema = 'public'
    GROUP BY table_schema, table_name
    ORDER BY table_name;
  "
)

for ITEM in $TABLES; do
  SCHEMA=$(echo "$ITEM" | cut -d'|' -f1)
  TABLE=$(echo "$ITEM" | cut -d'|' -f2)

  echo "Exportando ${SCHEMA}.${TABLE}..."

  COLUMNS=$(psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -Atc "
      SELECT string_agg(quote_ident(column_name), ', ' ORDER BY ordinal_position)
      FROM information_schema.columns
      WHERE table_schema = '$SCHEMA'
        AND table_name = '$TABLE';
    "
  )

  COUNT_ROWS=$(psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -Atc "
      SELECT COUNT(*)
      FROM \"$SCHEMA\".\"$TABLE\"
      WHERE registro = '$CNPJ';
    "
  )

  if [ "$COUNT_ROWS" -gt 0 ]; then
    echo "-- ${SCHEMA}.${TABLE} | linhas: ${COUNT_ROWS}" >> "$OUT_FILE"
    echo "COPY \"$SCHEMA\".\"$TABLE\" ($COLUMNS) FROM stdin;" >> "$OUT_FILE"

    psql \
      -h "$DB_HOST" \
      -p "$DB_PORT" \
      -U "$DB_USER" \
      -d "$DB_NAME" \
      -Atc "
        COPY (
          SELECT $COLUMNS
          FROM \"$SCHEMA\".\"$TABLE\"
          WHERE registro = '$CNPJ'
        ) TO STDOUT;
      " >> "$OUT_FILE"

    echo "\." >> "$OUT_FILE"
    echo "" >> "$OUT_FILE"
  fi
done

echo "COMMIT;" >> "$OUT_FILE"

echo "Dump criado em: $OUT_FILE"