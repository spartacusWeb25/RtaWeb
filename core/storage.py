import logging

from django.contrib.staticfiles.storage import StaticFilesStorage


logger = logging.getLogger("django")


class SafeStaticFilesStorage(StaticFilesStorage):
    """
    Evita quebra do collectstatic quando existir arquivo legado sem permissão de remoção.
    Em caso de PermissionError, mantém o arquivo atual e segue o processo.
    """

    def delete(self, name):
        try:
            return super().delete(name)
        except PermissionError:
            logger.warning(
                "⚠️ Sem permissão para remover arquivo estático '%s'. "
                "Mantendo arquivo existente e seguindo deploy.",
                name,
            )
            return
