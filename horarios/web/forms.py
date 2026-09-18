from django import forms
from django.core.exceptions import ValidationError
from horarios.models import Horarios


def _digits_only(valor) -> str:
    if valor is None:
        return ""
    return "".join(ch for ch in str(valor) if ch.isdigit())


def _safe_int(valor, default=0):
    try:
        if valor is None or valor == "":
            return default
        return int(str(valor).strip())
    except (TypeError, ValueError):
        d = _digits_only(valor)
        return int(d) if d else default


def _normalizar_horario(valor) -> str:
    if valor is None:
        return ""
    s = str(valor).strip()
    if not s:
        return ""
    s = s.replace(".", ":").replace("-", ":").replace(" ", "")
    digits = _digits_only(s)
    if len(digits) == 0:
        return ""
    if len(digits) == 1:
        return f"0{digits[0]}:00"
    if len(digits) == 2:
        return f"{digits[:2]}:00"
    if len(digits) == 3:
        return f"{digits[:2]}:{digits[2:3].ljust(2, '0')}"
    if len(digits) >= 4:
        return f"{digits[:2]}:{digits[2:4]}"
    return s


def _validar_horario_eh_valido(valor) -> bool:
    if valor is None:
        return True
    s = str(valor).strip()
    if not s:
        return True
    if ":" not in s:
        return False
    partes = s.split(":")
    if len(partes) < 2:
        return False
    try:
        hh = int(partes[0])
        mm = int(partes[1])
    except Exception:
        return False
    if hh < 0 or hh > 23:
        return False
    if mm < 0 or mm > 59:
        return False
    return True


_HORA_BASE_ATTRS = {
    "inputmode": "numeric",
    "maxlength": 5,
    "data-hora-mask": "true",
    "class": "form-control",
    "placeholder": "HH:MM",
}

_NUM_INT_ATTRS = {
    "inputmode": "numeric",
    "data-digits-only": "true",
    "class": "form-control",
}


_DIAS = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
_CAMPOS_HORA_POR_DIA = [
    "inic_1", "fina_1",
    "lanc_inic_1", "lanc_fina_1",
    "inic_2", "fina_2",
    "lanc_inic_2", "lanc_fina_2",
    "intervalo", "jornada",
]


class HorariosForm(forms.ModelForm):
    registro = forms.CharField(widget=forms.HiddenInput(), required=False)
    hora_empr = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    hora_fili = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    hora_codi = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Horarios
        fields = (
            "registro", "hora_empr", "hora_fili", "hora_codi",
            "hora_nome", "hora_flexivel", "hora_total_semana",
            "hora_folga_alt",
            "hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
            "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab",
            "hora_desc_esocial",
        )
        widgets = {
            "hora_nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: 08:00 12:00 13:00 17:48 ou Escritório",
            }),
            "hora_total_semana": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white text-center font-weight-bold",
                "readonly": True,
                "placeholder": "HH:MM (calculado)",
            }),
            "hora_desc_esocial": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": ("Segunda-feira, Terça-feira, Quarta-Feira, "
                                "Quinta-feira, Sexta-feira: 08:00 às 12:00 "
                                "e das 13:00 às 17:48"),
            }),
            "hora_flexivel": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_alt": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_dom": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_seg": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_ter": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_qua": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_qui": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_sex": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
            "hora_folga_sab": forms.CheckboxInput(attrs={"class": "form-check-input checkbox-folga"}),
        }
        labels = {
            "hora_nome": "Nome",
            "hora_flexivel": "Horário flexível",
            "hora_total_semana": "Total da semana",
            "hora_folga_alt": "Folga alternada",
            "hora_folga_dom": "Domingo",
            "hora_folga_seg": "Segunda",
            "hora_folga_ter": "Terça",
            "hora_folga_qua": "Quarta",
            "hora_folga_qui": "Quinta",
            "hora_folga_sex": "Sexta",
            "hora_folga_sab": "Sábado",
            "hora_desc_esocial": "Descrição da jornada para o eSocial",
        }

    def __init__(self, *args, banco="", db_alias="default", **kwargs):
        super().__init__(*args, **kwargs)
        self.banco = banco
        self.db_alias = db_alias
        instance = getattr(self, "instance", None)
        initial = getattr(self, "initial", None) or {}
        raw = {}

        # Carregar dados raw do banco ANTES de inicializar os campos hidden PK
        if banco and instance is not None:
            try:
                hora_codi = getattr(instance, "hora_codi", None)
                hora_empr = getattr(instance, "hora_empr", None)
                hora_fili = getattr(instance, "hora_fili", None)
                if hora_codi and banco:
                    from horarios.services.logic import HorariosService
                    empr = int(hora_empr or 1)
                    fili = int(hora_fili or 1)
                    raw = HorariosService.obter_quadro_raw(
                        banco=banco,
                        hora_codi=hora_codi,
                        db_alias=db_alias,
                        empr_codigo=empr,
                        fili_codigo=fili,
                    )
            except Exception:
                raw = {}

        # Garantir que os 4 campos hidden PK composta têm valores (mesmo required=False)
        pk_keys_defaults = [
            ("registro", _digits_only(banco) if banco else "", str),
            ("hora_empr", 1, int),
            ("hora_fili", 1, int),
            ("hora_codi", None, int),
        ]
        for chave, def_val, cast_f in pk_keys_defaults:
            val = None
            if raw and chave in raw and raw[chave] not in (None, ""):
                val = raw[chave]
            elif instance is not None:
                try:
                    val = getattr(instance, chave, None)
                except Exception:
                    val = None
            if val in (None, ""):
                val = initial.get(chave, def_val)
            if val in (None, "") and def_val is not None:
                val = def_val
            if val not in (None, ""):
                try:
                    str_val = str(val) if cast_f is str else str(cast_f(val))
                except Exception:
                    str_val = str(val)
                initial[chave] = val
                self.initial[chave] = val
                self.fields[chave].initial = val
                self.fields[chave].widget.attrs["value"] = str_val

        _DIAS_LOC = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
        _CAMPOS_LOC = [
            "inic_1", "fina_1",
            "lanc_inic_1", "lanc_fina_1",
            "inic_2", "fina_2",
            "lanc_inic_2", "lanc_fina_2",
            "intervalo", "jornada",
        ]

        for d in _DIAS_LOC:
            key_esoc = f"hora_{d}_esoc"
            self.fields[key_esoc] = forms.IntegerField(
                required=False,
                label="eSocial",
                widget=forms.NumberInput(attrs={
                    **_NUM_INT_ATTRS,
                    "placeholder": "1",
                }),
            )
            if key_esoc not in initial:
                val_get = None
                if raw and key_esoc in raw and raw[key_esoc] not in (None, ""):
                    val_get = raw[key_esoc]
                elif instance is not None:
                    try:
                        val_get = getattr(instance, key_esoc, None)
                    except Exception:
                        val_get = None
                if val_get is not None and val_get != "":
                    initial[key_esoc] = val_get
            val_esoc = initial.get(key_esoc, None)
            if val_esoc not in (None, ""):
                self.fields[key_esoc].initial = val_esoc
                self.initial[key_esoc] = val_esoc
                try:
                    self.fields[key_esoc].widget.attrs["value"] = str(int(val_esoc))
                except Exception:
                    self.fields[key_esoc].widget.attrs["value"] = str(val_esoc)

            for c in _CAMPOS_LOC:
                key = f"hora_{d}_{c}"
                attrs = {**_HORA_BASE_ATTRS}
                readonly = c in ("intervalo", "jornada")
                if readonly:
                    attrs["readonly"] = True
                    attrs["class"] = "form-control bg-secondary text-white text-center"
                    attrs["placeholder"] = "HH:MM"
                self.fields[key] = forms.CharField(
                    required=False,
                    max_length=10,
                    label="",
                    widget=forms.TextInput(attrs=attrs),
                )
                if key not in initial:
                    val_get = None
                    if raw and key in raw and raw[key] not in (None, ""):
                        val_get = str(raw[key])
                    elif instance is not None:
                        try:
                            val_get = getattr(instance, key, None)
                        except Exception:
                            val_get = None
                    if val_get not in (None, ""):
                        norm = _normalizar_horario(str(val_get))
                        if norm:
                            initial[key] = norm
                val_hora = initial.get(key, None)
                if val_hora not in (None, ""):
                    norm_val = _normalizar_horario(str(val_hora)) or str(val_hora)
                    self.fields[key].initial = norm_val
                    self.initial[key] = norm_val
                    self.fields[key].widget.attrs["value"] = norm_val

        extras = [
            "hora_nome", "hora_flexivel", "hora_total_semana",
            "hora_folga_alt", "hora_desc_esocial",
            "hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
            "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab",
        ]
        for key in extras:
            if key not in initial:
                val_ex = None
                if raw and key in raw and raw[key] not in (None, ""):
                    val_ex = raw[key]
                elif instance is not None:
                    try:
                        val_ex = getattr(instance, key, None)
                    except Exception:
                        val_ex = None
                if val_ex is None:
                    if key.startswith("hora_folga_") or key in ("hora_flexivel", "hora_folga_alt"):
                        val_ex = False
                if val_ex is not None:
                    initial[key] = val_ex
            val_extra = initial.get(key, None)
            if val_extra is None:
                if key.startswith("hora_folga_") or key in ("hora_flexivel", "hora_folga_alt"):
                    val_extra = False
                    initial[key] = False
            if key in self.fields and val_extra is not None:
                self.fields[key].initial = val_extra
                self.initial[key] = val_extra
                if key.startswith("hora_folga_") or key in ("hora_flexivel", "hora_folga_alt"):
                    try:
                        if bool(val_extra):
                            self.fields[key].widget.attrs["checked"] = True
                    except Exception:
                        pass
        self.initial = initial

    def _marcar_campo_invalido(self, field_name):
        f = self.fields.get(field_name)
        if not f:
            return
        widget = getattr(f, "widget", None)
        if widget is None:
            return
        attrs = getattr(widget, "attrs", None) or {}
        classes_orig = attrs.get("class") or ""
        class_list = [x for x in classes_orig.split(" ") if x] if classes_orig else []
        if "is-invalid" not in class_list:
            class_list.append("is-invalid")
        class_list = [x for x in class_list if x != "is-valid"]
        attrs["class"] = " ".join(class_list)
        widget.attrs = attrs

    def clean(self):
        cleaned = super().clean()
        campos_turno_e_lanche = [
            "inic_1", "fina_1",
            "lanc_inic_1", "lanc_fina_1",
            "inic_2", "fina_2",
            "lanc_inic_2", "lanc_fina_2",
        ]
        for d in _DIAS:
            chave_folga = f"hora_folga_{d}"
            val_folga = cleaned.get(chave_folga)
            try:
                eh_folga = bool(val_folga)
            except Exception:
                eh_folga = False
            if eh_folga:
                for c in _CAMPOS_HORA_POR_DIA:
                    chave = f"hora_{d}_{c}"
                    if chave in cleaned:
                        if c in ("intervalo", "jornada"):
                            cleaned[chave] = ""
                        else:
                            v = cleaned.get(chave)
                            if v in (None, ""):
                                continue
                            norm = _normalizar_horario(v)
                            cleaned[chave] = norm if norm else ""
                chave_esoc = f"hora_{d}_esoc"
                v_esoc = cleaned.get(chave_esoc)
                cleaned[chave_esoc] = _safe_int(v_esoc) if v_esoc not in (None, "") else None
                continue

            # Dias NÃO folga: verificar se TEM algum horário preenchido
            tem_algum = False
            for c in campos_turno_e_lanche:
                chave = f"hora_{d}_{c}"
                v = cleaned.get(chave)
                if v not in (None, ""):
                    norm = _normalizar_horario(v)
                    if norm:
                        tem_algum = True
                        break
            # Se NÃO tem nenhum horário preenchido neste dia NÃO folga:
            # Tudo bem! Limpa todos os campos deste dia (fica igual dia não cadastrado)
            if not tem_algum:
                for c in _CAMPOS_HORA_POR_DIA:
                    chave = f"hora_{d}_{c}"
                    cleaned[chave] = ""
                chave_esoc = f"hora_{d}_esoc"
                v_esoc = cleaned.get(chave_esoc)
                cleaned[chave_esoc] = _safe_int(v_esoc) if v_esoc not in (None, "") else None
                continue

            # Tem ALGUM horário preenchido: validar APENAS os campos que tem valor preenchido
            # (os demais podem ficar vazios normalmente)
            for c in _CAMPOS_HORA_POR_DIA:
                chave = f"hora_{d}_{c}"
                valor = cleaned.get(chave)
                if valor in (None, ""):
                    # Vazio é permitido (ex: turno 2 não existe) — não acusa erro
                    cleaned[chave] = ""
                    continue
                norm = _normalizar_horario(valor)
                if not norm:
                    cleaned[chave] = ""
                    continue
                if not _validar_horario_eh_valido(norm):
                    self.add_error(
                        chave,
                        f"Horário inválido para {d}.{c}: '{valor}'. Use HH:MM (00:00 até 23:59)."
                    )
                    self._marcar_campo_invalido(chave)
                else:
                    cleaned[chave] = norm
            chave_esoc = f"hora_{d}_esoc"
            v = cleaned.get(chave_esoc)
            cleaned[chave_esoc] = _safe_int(v) if v not in (None, "") else None
        return cleaned

    def validate_unique(self):
        banco_limpo = _digits_only(self.banco or "")
        empr = _safe_int(self.cleaned_data.get("hora_empr"))
        fili = _safe_int(self.cleaned_data.get("hora_fili"))
        codi = _safe_int(self.cleaned_data.get("hora_codi"))

        if not all([banco_limpo, empr, fili, codi]):
            return

        qs = Horarios.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            hora_empr=int(empr),
            hora_fili=int(fili),
            hora_codi=int(codi),
        )

        instance = getattr(self, "instance", None)
        is_editar = False
        if instance is not None:
            try:
                pk_parts = (
                    getattr(instance, "registro", None),
                    getattr(instance, "hora_empr", None),
                    getattr(instance, "hora_fili", None),
                    getattr(instance, "hora_codi", None),
                )
                is_editar = all(v is not None for v in pk_parts)
            except Exception:
                is_editar = False
        if is_editar:
            qs = qs.exclude(
                registro=getattr(instance, "registro"),
                hora_empr=getattr(instance, "hora_empr"),
                hora_fili=getattr(instance, "hora_fili"),
                hora_codi=getattr(instance, "hora_codi"),
            )
        if qs.exists():
            self.add_error(
                "hora_codi",
                (f"Já existe um Quadro de Horários com o Código {codi} "
                 f"para a Empresa/Filial selecionada."),
            )
            self._marcar_campo_invalido("hora_codi")
