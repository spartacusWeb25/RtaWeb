from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView
from terceiros.mixin import TerceiroMixin
from terceiros.services.logic import TerceirosService
from terceiros.utils import _has_errors


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class TerceiroUpdateView(TerceiroMixin, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar Terceiro"
        ctx["modo_edicao"] = True
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])

        # --- Grid dependentes (1:1 pattern do Funcionarios UpdateView) ---
        try:
            from dependentesterc.models import Dependentesterc

            if self.object and self.request.banco and self.request.db_alias:
                empr = getattr(self.object, "terc_empr", None)
                fili = getattr(self.object, "terc_fili", None)
                codi = getattr(self.object, "terc_codi", None)
                banco_formatado = self.request.banco
                banco_limpo = _digits_only(banco_formatado)
                print(f"[DEBUG Grid DepTerc] banco_formatado='{banco_formatado}' banco_limpo='{banco_limpo}' empr={empr} fili={fili} terc={codi}")
                if empr is not None and fili is not None and codi is not None:
                    qs = Dependentesterc.objects.using(self.request.db_alias)
                    # Padrao Funcionarios: tenta registro formatado (igual linha 31 funcionarios/web/views/atualizar.py)
                    deps = list(
                        qs.filter(
                            registro=banco_formatado,
                            depe_empr=int(empr),
                            depe_fili=int(fili),
                            depe_terc=int(codi),
                        )
                        .order_by("depe_codi")
                        .all()
                    )
                    # Fallback: se 0 com formatado, tenta apenas com digitos (ajuste de seguranca)
                    if len(deps) == 0:
                        print(f"[DEBUG Grid DepTerc] 0 com registro formatado, tentando limpo...")
                        deps = list(
                            Dependentesterc.objects.using(self.request.db_alias)
                            .filter(
                                registro=banco_limpo,
                                depe_empr=int(empr),
                                depe_fili=int(fili),
                                depe_terc=int(codi),
                            )
                            .order_by("depe_codi")
                            .all()
                        )
                        print(f"[DEBUG Grid DepTerc] fallback limpo retornou {len(deps)} linhas")
                    else:
                        print(f"[DEBUG Grid DepTerc] registro formatado retornou {len(deps)} linhas")
                    ctx["dependentes_list"] = deps
                    ctx["dependentes_qtd"] = len(deps)
                else:
                    print(f"[DEBUG Grid DepTerc] chave pai incompleta: empr={empr} fili={fili} codi={codi}")
                    ctx["dependentes_list"] = []
                    ctx["dependentes_qtd"] = 0
            else:
                print(f"[DEBUG Grid DepTerc] condições iniciais não atendidas: object={self.object is not None} banco={bool(self.request.banco)} db={bool(self.request.db_alias)}")
                ctx["dependentes_list"] = []
                ctx["dependentes_qtd"] = 0
        except Exception as exc:
            import traceback
            traceback.print_exc()
            print(f"[ERRO Grid DepTerc] {type(exc).__name__}: {exc}")
            messages.warning(self.request, f"Erro ao carregar grid dependentes: {type(exc).__name__} - {exc}")
            ctx["dependentes_list"] = []
            ctx["dependentes_qtd"] = 0

        return ctx

    def form_valid(self, form):
        try:
            terc_empr = self.obter_codigo_empresa_contexto(form=form)
            terc_fili = self.obter_codigo_filial_contexto(form=form)
            TerceirosService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                terc_empr=terc_empr,
                terc_fili=terc_fili,
                operacao="editar",  # ← PARÂMETRO EXPLÍCITO: É EDIÇÃO, NÃO BLOQUEIA DUPLICATA (é o mesmo registro)
            )
            messages.success(self.request, "Terceiro atualizado com sucesso.")
            return redirect(reverse("terceiros:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
