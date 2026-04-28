from django.shortcuts import get_object_or_404
from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.web.forms import FuncionarioForm


class FuncionarioMixin(BancoObrigatorioMixin):
    model = Funcionarios
    form_class = FuncionarioForm
    template_name = "funcionarios/funcionario_form.html"

    @property
    def db_alias(self) -> str:
        return self.request.db_alias

    def get_queryset(self):
        return Funcionarios.objects.using(self.db_alias).filter(
            registro=self.request.banco
        )

    def get_object(self, queryset=None):
        qs = queryset or self.get_queryset()
        obj = qs.filter(
            registro=self.request.banco,
            func_codi=self.kwargs["func_codi"],
        ).first()
        if obj is None:
            raise Http404
        return obj