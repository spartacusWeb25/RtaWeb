from django.db import IntegrityError


class RegistroDuplicadoError(Exception):
    def __init__(self, message="Registro já existe. Verifique os dados informados."):
        self.message = message
        super().__init__(self.message)

    @classmethod
    def tratar_integrity_error(cls, error):
        erro = str(error)

        if "duplicate key value violates unique constraint" in erro:
            return cls(
                "Já existe um lançamento com esses dados. Altere funcionário, referência ou evento."
            )

        return error
