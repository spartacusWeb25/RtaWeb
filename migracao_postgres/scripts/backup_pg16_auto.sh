#!/bin/bash

set -e

BACKUP_DIR="/backups"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "Backup automático iniciado."

while true; do
  DATA=$(date +"%Y-%m-%d_%H-%M-%S")
  ARQUIVO="$BACKUP_DIR/${POSTGRES_DB}_pg16_auto_${DATA}.dump"

  echo "Gerando backup: $ARQUIVO"

  pg_dump \
    -h postgres16 \
    -p 5432 \
    -U "$POSTGRES_USER" \
    -F c \
    -b \
    -v \
    -f "$ARQUIVO" \
    "$POSTGRES_DB"

  echo "Backup criado: $ARQUIVO"

  echo "Removendo backups com mais de $RETENTION_DAYS dias..."
  find "$BACKUP_DIR" -name "*_pg16_auto_*.dump" -type f -mtime +$RETENTION_DAYS -delete

  echo "Próximo backup em 24h."

  sleep 86400
done