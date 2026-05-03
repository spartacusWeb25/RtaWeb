#!/bin/bash

set -e

DATA=$(date +"%Y-%m-%d_%H-%M-%S")

PG10_HOST="${PG10_HOST:-127.0.0.1}"
PG10_PORT="${PG10_PORT:-5432}"
PG10_USER="${PG10_USER:-postgres}"
PG10_DB="${PG10_DB:-meubanco}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"

mkdir -p "$BACKUP_DIR"

ARQUIVO="$BACKUP_DIR/${PG10_DB}_pg10_${DATA}.dump"

echo "Iniciando backup do PostgreSQL 10..."
echo "Banco: $PG10_DB"
echo "Destino: $ARQUIVO"

pg_dump \
  -h "$PG10_HOST" \
  -p "$PG10_PORT" \
  -U "$PG10_USER" \
  -F c \
  -b \
  -v \
  -f "$ARQUIVO" \
  "$PG10_DB"

echo "Backup finalizado: $ARQUIVO"