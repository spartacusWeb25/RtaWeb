from django.db import models


class Adi(models.Model):
    id = models.AutoField(primary_key=True)
    nitem = models.IntegerField()
    di = models.CharField(max_length=12)
    i26_nadicao = models.IntegerField()
    i27_nseqadic = models.IntegerField(blank=True, null=True)
    i28_cfabricante = models.CharField(max_length=60, blank=True, null=True)
    i29_vdescdi = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    i29a_ndraw = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adi'


class Adtodecimo(models.Model):
    registro = models.CharField(max_length=14)
    adto_empr = models.IntegerField()
    adto_func = models.IntegerField()
    adto_ano = models.IntegerField()
    adto_data = models.DateField(blank=True, null=True)
    adto_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_perc_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_orig = models.CharField(max_length=1, blank=True, null=True)
    adto_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adtodecimo'


class Advertenciadisciplinar(models.Model):
    registro = models.CharField(max_length=14)
    adve_empr = models.IntegerField()
    adve_fili = models.IntegerField()
    adve_func = models.IntegerField()
    adve_ctrl = models.IntegerField()
    adve_data = models.DateField(blank=True, null=True)
    adve_moti = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advertenciadisciplinar'


class Afastamentosesocial(models.Model):
    moti_codi = models.CharField(max_length=2)
    moti_desc = models.CharField(max_length=350, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'afastamentosesocial'


class Caged(models.Model):
    cage_codi = models.IntegerField()
    cage_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caged'




class Cargos(models.Model):
    registro = models.CharField(max_length=14)
    carg_codi = models.IntegerField()
    carg_cbo = models.CharField(max_length=7, blank=True, null=True)
    carg_nome = models.CharField(max_length=60, blank=True, null=True)
    carg_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargos'


class Categoriasesocial(models.Model):
    cate_codi = models.IntegerField()
    cate_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoriasesocial'


class ContasferiasDecimo(models.Model):
    registro = models.CharField(max_length=14)
    cont_empr = models.IntegerField()
    cont_fili = models.IntegerField()
    cont_debi_feri = models.IntegerField(blank=True, null=True)
    cont_cred_feri = models.IntegerField(blank=True, null=True)
    cont_debi_deci = models.IntegerField(blank=True, null=True)
    cont_cred_deci = models.IntegerField(blank=True, null=True)
    cont_debi_feri_fgts = models.IntegerField(blank=True, null=True)
    cont_cred_feri_fgts = models.IntegerField(blank=True, null=True)
    cont_debi_deci_fgts = models.IntegerField(blank=True, null=True)
    cont_cred_deci_fgts = models.IntegerField(blank=True, null=True)
    cont_debi_feri_inss = models.IntegerField(blank=True, null=True)
    cont_cred_feri_inss = models.IntegerField(blank=True, null=True)
    cont_debi_deci_inss = models.IntegerField(blank=True, null=True)
    cont_cred_deci_inss = models.IntegerField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contasferias_decimo'


class Contasfolha(models.Model):
    registro = models.CharField(max_length=14)
    cont_empr = models.IntegerField()
    cont_even = models.IntegerField()
    cont_debi = models.IntegerField()
    cont_cred = models.IntegerField()
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    cont_fili = models.IntegerField()
    cont_dire = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'contasfolha'


class Dadosrescisao(models.Model):
    registro = models.CharField(max_length=14)
    dare_empr = models.IntegerField()
    dare_func = models.IntegerField()
    dare_data_avis = models.DateField(blank=True, null=True)
    dare_demi = models.DateField(blank=True, null=True)
    dare_dapa = models.DateField(blank=True, null=True)
    dare_tipo = models.IntegerField(blank=True, null=True)
    dare_sasa = models.BooleanField(blank=True, null=True)
    dare_avin = models.BooleanField(blank=True, null=True)
    dare_avpa = models.BooleanField(blank=True, null=True)
    dare_feri = models.BooleanField(blank=True, null=True)
    dare_de13 = models.BooleanField(blank=True, null=True)
    dare_fgmr = models.BooleanField(blank=True, null=True)
    dare_fgma = models.BooleanField(blank=True, null=True)
    dare_fgmu = models.BooleanField(blank=True, null=True)
    dare_grfc = models.BooleanField(blank=True, null=True)
    dare_mult = models.IntegerField(blank=True, null=True)
    dare_avis = models.IntegerField(blank=True, null=True)
    dare_perc_avis = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_perc_mult = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_sald_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dare_chav_iden = models.CharField(max_length=255, blank=True, null=True)
    dare_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    dare_refe = models.CharField(max_length=6, blank=True, null=True)
    dare_feri_prop = models.BooleanField(blank=True, null=True)
    dare_tipo_avis = models.IntegerField(blank=True, null=True)
    dare_moti_desl = models.CharField(max_length=2, blank=True, null=True)
    dare_inde_empr = models.BooleanField(blank=True, null=True)
    dare_term_avis = models.DateField(blank=True, null=True)
    dare_pens_alim = models.IntegerField(blank=True, null=True)
    dare_perc_pens_alim = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_valo_pens_alim = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dare_cert_obit = models.CharField(max_length=32, blank=True, null=True)
    dare_cump_avis_prev = models.IntegerField(blank=True, null=True)
    dare_naopagar112avos = models.BooleanField(blank=True, null=True)
    dare_func_trans_empr = models.BooleanField(blank=True, null=True)
    dare_func_trans_empr_tpinsc = models.IntegerField(blank=True, null=True)
    dare_func_trans_empr_nrinsc = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dadosrescisao'


class Departamentosrh(models.Model):
    registro = models.CharField(max_length=14)
    depa_empr = models.IntegerField()
    depa_codi = models.IntegerField()
    depa_nome = models.CharField(max_length=100, blank=True, null=True)
    depa_cnpj = models.CharField(max_length=14, blank=True, null=True)
    depa_cei = models.CharField(max_length=12, blank=True, null=True)
    depa_ende = models.CharField(max_length=60, blank=True, null=True)
    depa_nume = models.CharField(max_length=5, blank=True, null=True)
    depa_comp = models.CharField(max_length=10, blank=True, null=True)
    depa_cep = models.CharField(max_length=8, blank=True, null=True)
    depa_bair = models.CharField(max_length=60, blank=True, null=True)
    depa_ibge = models.CharField(max_length=7, blank=True, null=True)
    depa_cida = models.CharField(max_length=60, blank=True, null=True)
    depa_esta = models.CharField(max_length=2, blank=True, null=True)
    depa_fone = models.CharField(max_length=14, blank=True, null=True)
    depa_cecu = models.IntegerField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    depa_cnae = models.CharField(max_length=14, blank=True, null=True)
    depa_cno = models.CharField(max_length=14, blank=True, null=True)
    depa_inivalid = models.CharField(max_length=6, blank=True, null=True)
    depa_fimvalid = models.CharField(max_length=6, blank=True, null=True)
    depa_rat = models.IntegerField(blank=True, null=True)
    depa_fap = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    depa_indi_patr = models.IntegerField(blank=True, null=True)
    depa_cnpj_resp = models.CharField(max_length=14, blank=True, null=True)
    depa_lota_trib = models.CharField(max_length=30, blank=True, null=True)
    depa_fpas = models.CharField(max_length=3, blank=True, null=True)
    depa_codi_terc = models.CharField(max_length=4, blank=True, null=True)
    tp_inscprop = models.IntegerField(blank=True, null=True)
    nr_inscprop = models.CharField(max_length=15, blank=True, null=True)
    depa_obra_prop = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamentosrh'


class Dependentes(models.Model):
    depe_codi = models.CharField(max_length=2)
    depe_desc = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dependentes'


class Dependentesrh(models.Model):
    registro = models.CharField(max_length=14)
    depe_empr = models.IntegerField()
    depe_func = models.IntegerField()
    depe_nome = models.CharField(max_length=60, blank=True, null=True)
    depe_sexo = models.CharField(max_length=1, blank=True, null=True)
    depe_tipo = models.IntegerField(blank=True, null=True)
    depe_dana = models.DateField(blank=True, null=True)
    depe_sate = models.DateField(blank=True, null=True)
    depe_iate = models.DateField(blank=True, null=True)
    depe_pate = models.DateField(blank=True, null=True)
    depe_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    depe_codi = models.IntegerField()
    depe_cpf = models.CharField(max_length=11, blank=True, null=True)
    depe_inca = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dependentesrh'


class Desligamentosesocial(models.Model):
    desl_codi = models.CharField(max_length=2)
    desl_desc = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'desligamentosesocial'


class Distribuicaolucrosdividendosirrf(models.Model):
    registro = models.CharField(max_length=14)
    dist_empr = models.IntegerField()
    dist_enti = models.IntegerField()
    dist_ctrl = models.IntegerField()
    dist_data = models.DateField(blank=True, null=True)
    dist_serv = models.CharField(max_length=20, blank=True, null=True)
    dist_tota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dist_fili = models.IntegerField()
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    dist_rete_irrf = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dist_refe = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distribuicaolucrosdividendosirrf'


class Enviosesocial(models.Model):
    registro = models.CharField(max_length=14)
    envi_empr = models.IntegerField()
    envi_even = models.CharField(max_length=20)
    envi_form = models.CharField(max_length=7, blank=True, null=True)
    envi_ambi = models.SmallIntegerField()
    envi_prot = models.CharField(max_length=50)
    envi_item_codi = models.IntegerField()
    envi_item_tabe = models.CharField(max_length=20)
    envi_codi = models.IntegerField()
    envi_tipo = models.SmallIntegerField(blank=True, null=True)
    envi_data = models.DateTimeField(blank=True, null=True)
    envi_id_xml = models.BigIntegerField(blank=True, null=True)
    envi_refe = models.CharField(max_length=6, blank=True, null=True)
    envi_func = models.IntegerField(blank=True, null=True)
    envi_reci = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enviosesocial'


class Eventos(models.Model):
    registro = models.CharField(max_length=14)
    even_codi = models.IntegerField()
    even_desc = models.CharField(max_length=120, blank=True, null=True)
    even_irrf = models.BooleanField(blank=True, null=True)
    even_inss = models.BooleanField(blank=True, null=True)
    even_safa = models.BooleanField(blank=True, null=True)
    even_fgts = models.BooleanField(blank=True, null=True)
    even_refl = models.BooleanField(blank=True, null=True)
    even_medi = models.BooleanField(blank=True, null=True)
    even_insa = models.BooleanField(blank=True, null=True)
    even_peri = models.BooleanField(blank=True, null=True)
    even_rais = models.BooleanField(blank=True, null=True)
    even_tipo = models.CharField(max_length=1)
    even_form = models.CharField(max_length=1)
    even_peva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    even_dedu = models.BooleanField(blank=True, null=True)
    even_dere = models.CharField(max_length=2, blank=True, null=True)
    even_bpis = models.BooleanField(blank=True, null=True)
    even_naol = models.BooleanField(blank=True, null=True)
    even_notu = models.BooleanField(blank=True, null=True)
    even_gps = models.BooleanField(blank=True, null=True)
    even_cont = models.BooleanField(blank=True, null=True)
    even_bloq = models.BooleanField(blank=True, null=True)
    even_hera = models.BooleanField(blank=True, null=True)
    even_csra = models.BooleanField(blank=True, null=True)
    even_cara = models.BooleanField(blank=True, null=True)
    even_verb_resc = models.CharField(max_length=6, blank=True, null=True)
    even_plsa = models.BooleanField(blank=True, null=True)
    even_cnpj_plsa = models.CharField(max_length=14, blank=True, null=True)
    even_nome_plsa = models.CharField(max_length=150, blank=True, null=True)
    even_rans_plsa = models.CharField(max_length=6, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    even_empr = models.IntegerField()
    even_do_sist = models.BooleanField(blank=True, null=True)
    even_linh_clas = models.IntegerField(blank=True, null=True)
    even_base_hora_extr = models.BooleanField(blank=True, null=True)
    codinccp = models.IntegerField(blank=True, null=True)
    codincirrf = models.IntegerField(blank=True, null=True)
    codincfgts = models.IntegerField(blank=True, null=True)
    codincsind = models.IntegerField(blank=True, null=True)
    natrubr = models.CharField(max_length=6, blank=True, null=True)
    inivalid = models.CharField(max_length=6, blank=True, null=True)
    fimvalid = models.CharField(max_length=6, blank=True, null=True)
    even_dirf = models.CharField(max_length=6, blank=True, null=True)
    even_tipo_rubr = models.SmallIntegerField(blank=True, null=True)
    even_info_codi = models.BooleanField(blank=True, null=True)
    even_codi_esoc = models.CharField(max_length=6, blank=True, null=True)
    codinccprp = models.IntegerField(blank=True, null=True)
    codincpasep = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos'



class EventosPadrao(models.Model):
    registro = models.CharField(max_length=14, blank=True, null=True)
    even_codi = models.IntegerField(blank=True, null=True)
    even_desc = models.CharField(max_length=120, blank=True, null=True)
    even_irrf = models.BooleanField(blank=True, null=True)
    even_inss = models.BooleanField(blank=True, null=True)
    even_safa = models.BooleanField(blank=True, null=True)
    even_fgts = models.BooleanField(blank=True, null=True)
    even_refl = models.BooleanField(blank=True, null=True)
    even_medi = models.BooleanField(blank=True, null=True)
    even_insa = models.BooleanField(blank=True, null=True)
    even_peri = models.BooleanField(blank=True, null=True)
    even_rais = models.BooleanField(blank=True, null=True)
    even_tipo = models.CharField(max_length=1, blank=True, null=True)
    even_form = models.CharField(max_length=1, blank=True, null=True)
    even_peva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    even_dedu = models.BooleanField(blank=True, null=True)
    even_dere = models.CharField(max_length=2, blank=True, null=True)
    even_bpis = models.BooleanField(blank=True, null=True)
    even_naol = models.BooleanField(blank=True, null=True)
    even_notu = models.BooleanField(blank=True, null=True)
    even_gps = models.BooleanField(blank=True, null=True)
    even_dirf = models.CharField(max_length=6, blank=True, null=True)
    even_cont = models.BooleanField(blank=True, null=True)
    even_bloq = models.BooleanField(blank=True, null=True)
    even_hera = models.BooleanField(blank=True, null=True)
    even_csra = models.BooleanField(blank=True, null=True)
    even_cara = models.BooleanField(blank=True, null=True)
    even_verb_resc = models.CharField(max_length=6, blank=True, null=True)
    even_plsa = models.BooleanField(blank=True, null=True)
    even_cnpj_plsa = models.CharField(max_length=14, blank=True, null=True)
    even_nome_plsa = models.CharField(max_length=150, blank=True, null=True)
    even_rans_plsa = models.CharField(max_length=6, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    even_empr = models.IntegerField(blank=True, null=True)
    even_do_sist = models.BooleanField(blank=True, null=True)
    even_linh_clas = models.IntegerField(blank=True, null=True)
    even_natu_codi = models.IntegerField(blank=True, null=True)
    even_tipo_rubr = models.IntegerField(blank=True, null=True)
    codinccp = models.IntegerField(blank=True, null=True)
    codincirrf = models.IntegerField(blank=True, null=True)
    codincfgts = models.IntegerField(blank=True, null=True)
    codincsind = models.IntegerField(blank=True, null=True)
    codinccprp = models.IntegerField(blank=True, null=True)
    codincpasep = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos_padrao'


class Eventosesocial(models.Model):
    registro = models.CharField(max_length=14)
    even_empr = models.IntegerField()
    even_codi = models.IntegerField()
    natu_codi = models.IntegerField()
    codinccp = models.IntegerField(blank=True, null=True)
    codincirrf = models.IntegerField(blank=True, null=True)
    codincfgts = models.IntegerField(blank=True, null=True)
    codincsind = models.IntegerField(blank=True, null=True)
    even_tipo_rubr = models.SmallIntegerField(blank=True, null=True)
    codincpasep = models.IntegerField(blank=True, null=True)
    codinccprp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventosesocial'


class Eventospredefinidos(models.Model):
    registro = models.CharField(max_length=14)
    even_empr = models.IntegerField()
    even_even = models.IntegerField()
    even_refe_inic = models.CharField(max_length=6)
    even_refe_fina = models.CharField(max_length=6)
    even_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    even_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    even_func = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eventospredefinidos'


class EventospredefinidosBkp20210419(models.Model):
    registro = models.CharField(max_length=14, blank=True, null=True)
    even_empr = models.IntegerField(blank=True, null=True)
    even_fili = models.IntegerField(blank=True, null=True)
    even_even = models.IntegerField(blank=True, null=True)
    even_refe_inic = models.CharField(max_length=6, blank=True, null=True)
    even_refe_fina = models.CharField(max_length=6, blank=True, null=True)
    even_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    even_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    even_func = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventospredefinidos_bkp20210419'


class Fechamentofolha(models.Model):
    registro = models.CharField(max_length=14)
    fech_empr = models.IntegerField()
    fech_tipo_folh = models.CharField(max_length=2)
    fech_refe = models.CharField(max_length=6)
    fech_data = models.DateField(blank=True, null=True)
    fech_usua = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fechamentofolha'


class Fechamentorh(models.Model):
    registro = models.CharField(max_length=14)
    fech_empr = models.IntegerField()
    fech_tipo_folh = models.CharField(max_length=1)
    fech_refe = models.CharField(max_length=6)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fechamentorh'


class Ferias(models.Model):
    registro = models.CharField(max_length=14)
    feri_empr = models.IntegerField()
    feri_func = models.IntegerField()
    feri_refe = models.CharField(max_length=6)
    feri_sequ = models.IntegerField()
    feri_data_avis = models.DateField(blank=True, null=True)
    feri_data_reci = models.DateField(blank=True, null=True)
    feri_data_paga = models.DateField(blank=True, null=True)
    feri_medi_hora = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_medi_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_sala_mens = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_sala_hora = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_aqui_inic = models.DateField(blank=True, null=True)
    feri_aqui_fina = models.DateField(blank=True, null=True)
    feri_falt = models.IntegerField(blank=True, null=True)
    feri_novo_aqui_inic = models.DateField(blank=True, null=True)
    feri_novo_aqui_fina = models.DateField(blank=True, null=True)
    feri_feri_inic = models.DateField(blank=True, null=True)
    feri_feri_fina = models.DateField(blank=True, null=True)
    feri_dias_feri = models.IntegerField(blank=True, null=True)
    feri_abon_inic = models.DateField(blank=True, null=True)
    feri_abon_fina = models.DateField(blank=True, null=True)
    feri_dias_abon = models.IntegerField(blank=True, null=True)
    feri_dias_sala_1 = models.IntegerField(blank=True, null=True)
    feri_sala_refe_1 = models.CharField(max_length=6, blank=True, null=True)
    feri_dias_sala_2 = models.IntegerField(blank=True, null=True)
    feri_sala_refe_2 = models.CharField(max_length=6, blank=True, null=True)
    feri_deci_terc = models.BooleanField(blank=True, null=True)
    feri_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    feri_refe_folh = models.CharField(max_length=6, blank=True, null=True)
    feri_feri_base_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_feri_valo_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_terc_valo_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_feri_base_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_feri_valo_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_terc_valo_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_base_inss_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_base_inss_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_inss_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_inss_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_base_irrf = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_irrf = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_faix_irrf = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_depe_irrf = models.IntegerField(blank=True, null=True)
    feri_base_abon_pecu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_abon_pecu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_medi_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_medi_hora = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_mese_medi = models.IntegerField(blank=True, null=True)
    feri_terc_abon_pecu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_deci_terc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_aliq_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_fgts_deci = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_medi_valo_deci = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_valo_medi_hora_deci = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_adic_temp_serv_ferias = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_adic_temp_serv_13feri = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_adic_temp_serv_ferias2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_adic_temp_serv_13feri2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_peri_valo_refe_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_peri_valo_refe_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_pens_alim = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_base_pens_alim = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_desc_empr_cons = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_base_desc_empr_cons = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    feri_grat_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ferias'


class Folhaadtodecimo(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folhaadtodecimo'


class Folhadecimo(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folhadecimo'


class Folhaferias(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_sequ = models.IntegerField()
    fome_ctrl = models.CharField(max_length=1)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folhaferias'


class Folhamensal(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folhamensal'


class Folhaquinzenal(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folhaquinzenal'


class Folharescisao(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folharescisao'


class Folharescisaocomplementar(models.Model):
    registro = models.CharField(max_length=14)
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'folharescisaocomplementar'


class Formulasfuncionario(models.Model):
    registro = models.CharField(max_length=14)
    form_empr = models.IntegerField()
    form_func = models.IntegerField()
    form_sequ = models.IntegerField()
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formulasfuncionario'


class FormulasfuncionarioBkp20210419(models.Model):
    registro = models.CharField(max_length=14, blank=True, null=True)
    form_empr = models.IntegerField(blank=True, null=True)
    form_fili = models.IntegerField(blank=True, null=True)
    form_func = models.IntegerField(blank=True, null=True)
    form_sequ = models.IntegerField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formulasfuncionario_bkp20210419'


class Formulasrh(models.Model):
    registro = models.CharField(max_length=14)
    form_empr = models.IntegerField()
    form_codi = models.IntegerField()
    form_desc = models.CharField(max_length=60, blank=True, null=True)
    form_even = models.IntegerField(blank=True, null=True)
    form_form = models.TextField(blank=True, null=True)
    form_feri = models.BooleanField(blank=True, null=True)
    form_resc = models.BooleanField(blank=True, null=True)
    form_adto = models.BooleanField(blank=True, null=True)
    form_fome = models.BooleanField(blank=True, null=True)
    form_ad13 = models.BooleanField(blank=True, null=True)
    form_desa = models.BooleanField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formulasrh'


class Funcionarios(models.Model):
    registro = models.CharField(max_length=14)
    func_empr = models.IntegerField()
    func_fili = models.IntegerField()
    func_codi = models.IntegerField()
    func_regi = models.CharField(max_length=30, blank=True, null=True)
    func_nome = models.CharField(max_length=60, blank=True, null=True)
    func_sexo = models.CharField(max_length=1, blank=True, null=True)
    func_dana = models.DateField(blank=True, null=True)
    func_cpf = models.CharField(max_length=11, blank=True, null=True)
    func_pis = models.CharField(max_length=11, blank=True, null=True)
    func_ende = models.CharField(max_length=60, blank=True, null=True)
    func_bair = models.CharField(max_length=60, blank=True, null=True)
    func_cep = models.CharField(max_length=8, blank=True, null=True)
    func_pai = models.CharField(max_length=60, blank=True, null=True)
    func_mae = models.CharField(max_length=60, blank=True, null=True)
    func_esci = models.CharField(max_length=1, blank=True, null=True)
    func_deir = models.IntegerField(blank=True, null=True)
    func_desa = models.IntegerField(blank=True, null=True)
    func_anch = models.CharField(max_length=4, blank=True, null=True)
    func_daad = models.DateField(blank=True, null=True)
    func_tiad = models.IntegerField(blank=True, null=True)
    func_demi = models.DateField(blank=True, null=True)
    func_tide = models.IntegerField(blank=True, null=True)
    func_tisa = models.CharField(max_length=1, blank=True, null=True)
    func_home = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_hose = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_saho = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    func_fopa = models.CharField(max_length=1, blank=True, null=True)
    func_adqu = models.BooleanField(blank=True, null=True)
    func_insa = models.BooleanField(blank=True, null=True)
    func_peri = models.BooleanField(blank=True, null=True)
    func_banc_paga = models.IntegerField(blank=True, null=True)
    func_cont_paga = models.CharField(max_length=11, blank=True, null=True)
    func_cont_fgts = models.CharField(max_length=11, blank=True, null=True)
    func_inss = models.BooleanField(blank=True, null=True)
    func_fgts = models.BooleanField(blank=True, null=True)
    func_irrf = models.BooleanField(blank=True, null=True)
    func_depa = models.IntegerField(blank=True, null=True)
    func_seto = models.IntegerField(blank=True, null=True)
    func_carg = models.IntegerField(blank=True, null=True)
    func_sind = models.IntegerField(blank=True, null=True)
    func_ibge = models.CharField(max_length=7, blank=True, null=True)
    func_grin = models.CharField(max_length=2, blank=True, null=True)
    func_cbo = models.CharField(max_length=6, blank=True, null=True)
    func_naci = models.CharField(max_length=2, blank=True, null=True)
    func_raca = models.CharField(max_length=1, blank=True, null=True)
    func_vinc = models.CharField(max_length=2, blank=True, null=True)
    func_ctps = models.CharField(max_length=11, blank=True, null=True)
    func_seri_ctps = models.CharField(max_length=5, blank=True, null=True)
    func_esta_ctps = models.CharField(max_length=2, blank=True, null=True)
    func_emis_ctps = models.DateField(blank=True, null=True)
    func_defi = models.CharField(max_length=1, blank=True, null=True)
    func_titu = models.CharField(max_length=14, blank=True, null=True)
    func_digi_titu = models.CharField(max_length=2, blank=True, null=True)
    func_zona_titu = models.CharField(max_length=5, blank=True, null=True)
    func_seca_titu = models.CharField(max_length=5, blank=True, null=True)
    func_regi_prof = models.CharField(max_length=20, blank=True, null=True)
    func_regi_cate = models.CharField(max_length=30, blank=True, null=True)
    func_regi_vali = models.DateField(blank=True, null=True)
    func_venc_exam = models.DateField(blank=True, null=True)
    func_sala_cont = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_tisa_rais = models.CharField(max_length=1, blank=True, null=True)
    func_cate_sefi = models.IntegerField(blank=True, null=True)
    func_ocor_sefi = models.IntegerField(blank=True, null=True)
    func_celu = models.CharField(max_length=14, blank=True, null=True)
    func_emai = models.CharField(max_length=100, blank=True, null=True)
    func_rege = models.CharField(max_length=15, blank=True, null=True)
    func_rege_orga = models.CharField(max_length=6, blank=True, null=True)
    func_rege_expe = models.DateField(blank=True, null=True)
    func_cnh = models.CharField(max_length=20, blank=True, null=True)
    func_cate = models.CharField(max_length=2, blank=True, null=True)
    func_cnh_prim = models.DateField(blank=True, null=True)
    func_cnh_emis = models.DateField(blank=True, null=True)
    func_cnh_vali = models.DateField(blank=True, null=True)
    func_daop_fgts = models.DateField(blank=True, null=True)
    func_esta = models.CharField(max_length=2, blank=True, null=True)
    func_foto = models.TextField(blank=True, null=True)
    func_cose = models.CharField(max_length=3, blank=True, null=True)
    func_alva = models.IntegerField(blank=True, null=True)
    func_pens = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_fone_dive = models.CharField(max_length=30, blank=True, null=True)
    func_dia1 = models.IntegerField(blank=True, null=True)
    func_ven1 = models.DateField(blank=True, null=True)
    func_dia2 = models.IntegerField(blank=True, null=True)
    func_ven2 = models.DateField(blank=True, null=True)
    func_refe_desc_sind = models.CharField(max_length=6, blank=True, null=True)
    func_en01 = models.TimeField(blank=True, null=True)
    func_sa01 = models.TimeField(blank=True, null=True)
    func_en02 = models.TimeField(blank=True, null=True)
    func_sa02 = models.TimeField(blank=True, null=True)
    func_func_sind = models.BooleanField(blank=True, null=True)
    func_tipo_defi = models.IntegerField(blank=True, null=True)
    func_catr = models.IntegerField(blank=True, null=True)
    func_data_cada = models.DateField(blank=True, null=True)
    func_data_alte = models.DateField(blank=True, null=True)
    func_norm = models.IntegerField(blank=True, null=True)
    func_saba = models.IntegerField(blank=True, null=True)
    func_domi = models.IntegerField(blank=True, null=True)
    func_feri = models.IntegerField(blank=True, null=True)
    func_rege_uf = models.CharField(max_length=2, blank=True, null=True)
    func_loca = models.CharField(max_length=30, blank=True, null=True)
    func_loca_uf = models.CharField(max_length=2, blank=True, null=True)
    func_regi_casa = models.IntegerField(blank=True, null=True)
    func_tipo_cred = models.IntegerField(blank=True, null=True)
    func_matr = models.IntegerField(blank=True, null=True)
    func_base_insa = models.IntegerField(blank=True, null=True)
    func_inat = models.BooleanField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    func_apre = models.BooleanField(blank=True, null=True)
    func_agen = models.CharField(max_length=11, blank=True, null=True)
    func_nume = models.CharField(max_length=5, blank=True, null=True)
    func_comp = models.CharField(max_length=20, blank=True, null=True)
    func_perc_insa = models.IntegerField(blank=True, null=True)
    func_insa_sobr = models.IntegerField(blank=True, null=True)
    func_natu = models.CharField(max_length=60, blank=True, null=True)
    func_uf_natu = models.CharField(max_length=2, blank=True, null=True)
    func_exam_data = models.DateField(blank=True, null=True)
    func_exam_codi = models.CharField(max_length=17, blank=True, null=True)
    func_exam_cnpj = models.CharField(max_length=14, blank=True, null=True)
    func_exam_crm = models.CharField(max_length=10, blank=True, null=True)
    func_exam_crm_uf = models.CharField(max_length=2, blank=True, null=True)
    func_cate_esoc = models.IntegerField(blank=True, null=True)
    func_jorn = models.SmallIntegerField(blank=True, null=True)
    func_noso = models.CharField(max_length=60, blank=True, null=True)
    func_pais_nasc = models.CharField(max_length=7, blank=True, null=True)
    func_pais_naci = models.CharField(max_length=7, blank=True, null=True)
    func_rne = models.CharField(max_length=14, blank=True, null=True)
    func_rne_emis = models.CharField(max_length=20, blank=True, null=True)
    func_rne_expe = models.DateField(blank=True, null=True)
    func_cnh_esta = models.CharField(max_length=2, blank=True, null=True)
    func_tipo_logr = models.CharField(max_length=4, blank=True, null=True)
    func_extr_cond = models.IntegerField(blank=True, null=True)
    func_extr_data_cheg = models.DateField(blank=True, null=True)
    func_extr_casa_bras = models.BooleanField(blank=True, null=True)
    func_extr_filh_bras = models.BooleanField(blank=True, null=True)
    func_defi_cota = models.BooleanField(blank=True, null=True)
    func_apos = models.BooleanField(blank=True, null=True)
    func_esoc_tipo_admi = models.IntegerField(blank=True, null=True)
    func_esoc_indi_admi = models.IntegerField(blank=True, null=True)
    func_natu_ativ = models.IntegerField(blank=True, null=True)
    func_esoc_regi_jorn = models.IntegerField(blank=True, null=True)
    func_regi_prev = models.IntegerField(blank=True, null=True)
    func_tipo_cont = models.IntegerField(blank=True, null=True)
    func_data_term_cont = models.DateField(blank=True, null=True)
    func_cont_temp_parc = models.IntegerField(blank=True, null=True)
    func_codi_lota_trib = models.CharField(max_length=15, blank=True, null=True)
    func_insa_sobr_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_esoc_tipo_insc = models.IntegerField(blank=True, null=True)
    func_esoc_nume_insc = models.CharField(max_length=15, blank=True, null=True)
    func_esoc_matr_ante = models.CharField(max_length=30, blank=True, null=True)
    func_esoc_tran_obse = models.CharField(max_length=255, blank=True, null=True)
    func_esoc_data_tran = models.DateField(blank=True, null=True)
    func_vale_alim = models.BooleanField(blank=True, null=True)
    func_valo_diar = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    func_cate_tpinsc = models.IntegerField(blank=True, null=True)
    func_cate_nrinsc = models.CharField(max_length=14, blank=True, null=True)
    func_temp_resi = models.IntegerField(blank=True, null=True)
    func_apren_contr_dire = models.IntegerField(blank=True, null=True)
    func_apren_enti_qual = models.CharField(max_length=14, blank=True, null=True)
    func_indi_contr = models.IntegerField(blank=True, null=True)
    func_esta_natu_esta = models.IntegerField(blank=True, null=True)
    func_esta_nive_esta = models.IntegerField(blank=True, null=True)
    func_esta_data_term = models.DateField(blank=True, null=True)
    func_esta_inst_ensi = models.CharField(max_length=14, blank=True, null=True)
    func_tp_rein = models.IntegerField(blank=True, null=True)
    func_num_proc = models.CharField(max_length=20, blank=True, null=True)
    func_lei_anis = models.CharField(max_length=13, blank=True, null=True)
    func_data_efet_reto = models.DateField(blank=True, null=True)
    func_data_efeito = models.DateField(blank=True, null=True)
    func_cons_fgts_inst = models.CharField(max_length=3, blank=True, null=True)
    func_cons_fgts_contr = models.CharField(max_length=15, blank=True, null=True)
    func_remu_outr_tpinsc = models.IntegerField(blank=True, null=True)
    func_remu_outr_nrinsc = models.CharField(max_length=14, blank=True, null=True)
    func_remu_outr_cate = models.IntegerField(blank=True, null=True)
    func_remu_outr_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_remu_outr_indi = models.IntegerField(blank=True, null=True)
    func_cons_fgts_even = models.IntegerField(blank=True, null=True)
    func_cons_fgts_inst2 = models.CharField(max_length=3, blank=True, null=True)
    func_cons_fgts_contr2 = models.CharField(max_length=12, blank=True, null=True)
    func_cons_fgts_even2 = models.IntegerField(blank=True, null=True)
    func_cons_fgts_even3 = models.IntegerField(blank=True, null=True)
    func_cons_fgts_contr3 = models.CharField(max_length=12, blank=True, null=True)
    func_cons_fgts_inst3 = models.CharField(max_length=3, blank=True, null=True)
    func_cons_fgts_even4 = models.IntegerField(blank=True, null=True)
    func_cons_fgts_inst4 = models.CharField(max_length=3, blank=True, null=True)
    func_cons_fgts_contr4 = models.CharField(max_length=12, blank=True, null=True)
    func_data_expi_exam_ocup = models.DateField(blank=True, null=True)
    func_tipo_exam_ocup = models.IntegerField(blank=True, null=True)
    func_vale_trans = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funcionarios'


class Histfolha(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    historico = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'histfolha'


class Historicodeferias(models.Model):
    registro = models.CharField(max_length=14)
    hist_empr = models.IntegerField()
    hist_func = models.IntegerField()
    hist_refe = models.CharField(max_length=6)
    hist_sequ = models.IntegerField()
    hist_aqui_inic = models.DateField(blank=True, null=True)
    hist_aqui_fina = models.DateField(blank=True, null=True)
    hist_gozo_inic = models.DateField(blank=True, null=True)
    hist_gozo_fina = models.DateField(blank=True, null=True)
    hist_dias_gozo = models.IntegerField(blank=True, null=True)
    hist_inic_abon = models.DateField(blank=True, null=True)
    hist_term_abon = models.DateField(blank=True, null=True)
    hist_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    hist_dias_abon = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historicodeferias'


class Horarios(models.Model):
    registro = models.CharField(max_length=14)
    hora_prof = models.IntegerField()
    hora_dia = models.IntegerField()
    hora_inic_1 = models.TimeField(blank=True, null=True)
    hora_fina_1 = models.TimeField(blank=True, null=True)
    hora_inic_2 = models.TimeField(blank=True, null=True)
    hora_fina_2 = models.TimeField(blank=True, null=True)
    hora_inic_3 = models.TimeField(blank=True, null=True)
    hora_fina_3 = models.TimeField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    hora_data = models.DateField()
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'horarios'


class Horariospadrao(models.Model):
    registro = models.CharField(max_length=14)
    hora_codi_padr = models.IntegerField()
    hora_desc_padr = models.CharField(max_length=100, blank=True, null=True)
    hora_peri_1_ini = models.TimeField(blank=True, null=True)
    hora_peri_1_fim = models.TimeField(blank=True, null=True)
    hora_peri_2_ini = models.TimeField(blank=True, null=True)
    hora_peri_2_fim = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horariospadrao'


class Jornada(models.Model):
    registro = models.CharField(max_length=14)
    jorn_codi = models.IntegerField()
    jorn_nome = models.CharField(max_length=100)
    jorn_tipo = models.SmallIntegerField()
    jorn_hora_sema = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jorn_notu = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jornada'


class JornadaHorarios(models.Model):
    registro = models.CharField(max_length=14)
    jorn_codi = models.IntegerField()
    hora_dia = models.CharField(max_length=3)
    hora_tipo = models.SmallIntegerField()
    hora_peri_1_ini = models.TimeField(blank=True, null=True)
    hora_peri_1_fim = models.TimeField(blank=True, null=True)
    hora_peri_2_ini = models.TimeField(blank=True, null=True)
    hora_peri_2_fim = models.TimeField(blank=True, null=True)
    hora_prin = models.BooleanField(blank=True, null=True)
    hora_codi_padr = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jornada_horarios'


class Lancamentosdecimo(models.Model):
    registro = models.CharField(max_length=14)
    lafo_empr = models.SmallIntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_func = models.IntegerField()
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lancamentosdecimo'


class Lancamentosferias(models.Model):
    registro = models.CharField(max_length=14)
    lafo_empr = models.IntegerField()
    lafo_func = models.IntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_refe_folh = models.CharField(max_length=6, blank=True, null=True)
    lafo_sequ = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lancamentosferias'


class Lancamentosfolha(models.Model):
    registro = models.CharField(max_length=14)
    lafo_empr = models.SmallIntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_func = models.IntegerField()
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lancamentosfolha'


class Lctofolhamensal(models.Model):
    registro = models.CharField(max_length=14)
    lanc_empr = models.IntegerField()
    lanc_func = models.IntegerField()
    lanc_refe = models.CharField(max_length=6)
    lanc_even = models.IntegerField()
    lanc_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lanc_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lanc_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lanc_tipo = models.CharField(max_length=1, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lanc_obse = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lctofolhamensal'


class Lctorescisao(models.Model):
    registro = models.CharField(max_length=14)
    lafo_empr = models.SmallIntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_func = models.IntegerField()
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lctorescisao'


class Lctorescisaocomplementar(models.Model):
    registro = models.CharField(max_length=14)
    lafo_empr = models.SmallIntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_func = models.IntegerField()
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lctorescisaocomplementar'


class Linhavaletransporte(models.Model):
    registro = models.CharField(max_length=14)
    linh_empr = models.IntegerField()
    linh_codi = models.IntegerField()
    linh_desc = models.CharField(max_length=60, blank=True, null=True)
    linh_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    linh_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linhavaletransporte'




class Paisesesocial(models.Model):
    pais_codi = models.CharField(max_length=3)
    pais_nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'paisesesocial'


class Processoseventos(models.Model):
    registro = models.CharField(max_length=14)
    even_codi = models.IntegerField()
    tpproc = models.IntegerField(blank=True, null=True)
    nrproc = models.CharField(max_length=21, blank=True, null=True)
    extdecisao = models.IntegerField(blank=True, null=True)
    codsusp = models.CharField(max_length=14, blank=True, null=True)
    nrprocIr = models.CharField(max_length=21, blank=True, null=True)
    codsuspir = models.CharField(max_length=14, blank=True, null=True)
    nrprocfg = models.CharField(max_length=21, blank=True, null=True)
    nrprocsind = models.CharField(max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'processoseventos'


class Procvaletransporte(models.Model):
    registro = models.CharField(max_length=14)
    proc_empr = models.IntegerField()
    proc_fili = models.IntegerField()
    proc_func = models.IntegerField()
    proc_refe = models.CharField(max_length=6)
    proc_linh = models.IntegerField()
    proc_tota_vale = models.IntegerField(blank=True, null=True)
    proc_valo_linh = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    proc_tota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'procvaletransporte'


class Rais(models.Model):
    rais_codi = models.IntegerField()
    rais_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rais'


class Raisdemi(models.Model):
    rais_codi = models.IntegerField()
    rais_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raisdemi'


class Sefip(models.Model):
    sefi_codi = models.IntegerField()
    sefi_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sefip'


class Sefipmes(models.Model):
    registro = models.CharField(max_length=14)
    sefi_empr = models.IntegerField()
    sefi_fili = models.IntegerField()
    sefi_refe = models.CharField(max_length=6)
    sefi_core = models.CharField(max_length=3)
    sefi_raza = models.CharField(max_length=32, blank=True, null=True)
    sefi_cgcm = models.CharField(max_length=14, blank=True, null=True)
    sefi_ceii = models.CharField(max_length=14, blank=True, null=True)
    sefi_ende = models.CharField(max_length=32, blank=True, null=True)
    sefi_bair = models.CharField(max_length=20, blank=True, null=True)
    sefi_cepo = models.FloatField(blank=True, null=True)
    sefi_cida = models.CharField(max_length=20, blank=True, null=True)
    sefi_esta = models.CharField(max_length=2, blank=True, null=True)
    sefi_dddf = models.CharField(max_length=4, blank=True, null=True)
    sefi_fone = models.CharField(max_length=8, blank=True, null=True)
    sefi_aend = models.CharField(max_length=1, blank=True, null=True)
    sefi_asat = models.FloatField(blank=True, null=True)
    sefi_cent = models.FloatField(blank=True, null=True)
    sefi_ccef = models.FloatField(blank=True, null=True)
    sefi_opta = models.FloatField(blank=True, null=True)
    sefi_fpas = models.FloatField(blank=True, null=True)
    sefi_cote = models.FloatField(blank=True, null=True)
    sefi_sala = models.FloatField(blank=True, null=True)
    sefi_banc = models.FloatField(blank=True, null=True)
    sefi_agen = models.FloatField(blank=True, null=True)
    sefi_corr = models.CharField(max_length=9, blank=True, null=True)
    sefi_ccus = models.CharField(max_length=4, blank=True, null=True)
    sefi_13ma = models.FloatField(blank=True, null=True)
    sefi_even = models.FloatField(blank=True, null=True)
    sefi_orig = models.CharField(max_length=1, blank=True, null=True)
    sefi_rurf = models.FloatField(blank=True, null=True)
    sefi_rurj = models.FloatField(blank=True, null=True)
    sefi_obs1 = models.CharField(max_length=7, blank=True, null=True)
    sefi_proc = models.FloatField(blank=True, null=True)
    sefi_vara = models.FloatField(blank=True, null=True)
    sefi_pini = models.CharField(max_length=6, blank=True, null=True)
    sefi_pfin = models.CharField(max_length=6, blank=True, null=True)
    sefi_comp = models.FloatField(blank=True, null=True)
    sefi_cini = models.CharField(max_length=6, blank=True, null=True)
    sefi_cfin = models.CharField(max_length=6, blank=True, null=True)
    sefi_aseg = models.FloatField(blank=True, null=True)
    sefi_aemp = models.FloatField(blank=True, null=True)
    sefi_ater = models.FloatField(blank=True, null=True)
    sefi_aded = models.FloatField(blank=True, null=True)
    sefi_pcom = models.CharField(max_length=6, blank=True, null=True)
    sefi_fcom = models.CharField(max_length=6, blank=True, null=True)
    sefi_acna = models.CharField(max_length=1, blank=True, null=True)
    sefi_gera = models.CharField(max_length=1, blank=True, null=True)
    sefi_fg13 = models.CharField(max_length=1, blank=True, null=True)
    sefi_me13 = models.CharField(max_length=6, blank=True, null=True)
    sefi_bafg = models.FloatField(blank=True, null=True)
    sefi_cgps = models.FloatField(blank=True, null=True)
    sefi_emre = models.FloatField(blank=True, null=True)
    sefi_tifg = models.FloatField(blank=True, null=True)
    sefi_dafg = models.DateField(blank=True, null=True)
    sefi_tiin = models.FloatField(blank=True, null=True)
    sefi_dain = models.DateField(blank=True, null=True)
    sefi_iain = models.FloatField(blank=True, null=True)
    sefi_sama = models.FloatField(blank=True, null=True)
    sefi_dr13 = models.FloatField(blank=True, null=True)
    sefi_vdpr = models.FloatField(blank=True, null=True)
    sefi_tipo_insc = models.CharField(max_length=1, blank=True, null=True)
    sefi_cnpj_ceii = models.CharField(max_length=14, blank=True, null=True)
    sefi_moda = models.IntegerField(blank=True, null=True)
    sefi_simp = models.IntegerField(blank=True, null=True)
    sefi_oude = models.FloatField(blank=True, null=True)
    sefi_cont = models.CharField(max_length=20, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sefipmes'


class Setoresrh(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    seto_empr = models.IntegerField()
    seto_codi = models.IntegerField()
    seto_desc = models.CharField(max_length=60, blank=True, null=True)
    seto_sigl = models.CharField(max_length=5, blank=True, null=True)
    seto_cecu = models.IntegerField(blank=True, null=True)
    seto_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'setoresrh'


class Sindicatos(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    sind_codi = models.IntegerField()
    sind_nome = models.CharField(max_length=100, blank=True, null=True)
    sind_cnpj = models.CharField(max_length=14, blank=True, null=True)
    sind_codi_sind = models.CharField(max_length=15, blank=True, null=True)
    sind_cida = models.CharField(max_length=60, blank=True, null=True)
    sind_esta = models.CharField(max_length=2, blank=True, null=True)
    sind_fone = models.CharField(max_length=14, blank=True, null=True)
    sind_emai = models.CharField(max_length=100, blank=True, null=True)
    sind_mes_conv = models.IntegerField(blank=True, null=True)
    sind_perc_desc_mens = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sind_max_desc_vt = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sind_mese_medi = models.IntegerField(blank=True, null=True)
    sind_even_desc = models.IntegerField(blank=True, null=True)
    sind_piso_cate = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    sind_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    sind_adic_temp_serv = models.BooleanField(blank=True, null=True)
    sind_medi_feri = models.IntegerField(blank=True, null=True)
    sind_porc_adic = models.IntegerField(blank=True, null=True)
    sind_peri_adic = models.IntegerField(blank=True, null=True)
    sind_porc_adic_maxi = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sindicatos'




class Tipodemissaocaged(models.Model):
    cade_codi = models.CharField(max_length=2)
    cade_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipodemissaocaged'


class Tipodemissaorais(models.Model):
    cade_codi = models.CharField(max_length=2)
    cade_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipodemissaorais'


class Tipodemissaosefip(models.Model):
    cade_codi = models.CharField(max_length=2)
    cade_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipodemissaosefip'


class Valerefeicao(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    vare_empr = models.IntegerField()
    vare_refe = models.CharField(max_length=6)
    vare_sa01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_sa02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_sa03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_sa04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_sa05 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_em01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_em02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_em03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_em04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_em05 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_fu01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_fu02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_fu03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_fu04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_fu05 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    vare_vare = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valerefeicao'


class Valetransporte(models.Model):
    registro = models.CharField(max_length=14)
    quav_empr = models.IntegerField()
    quav_fili = models.IntegerField()
    quav_func = models.IntegerField()
    quav_linh = models.IntegerField()
    quav_refe = models.CharField(max_length=6)
    quav_norm = models.IntegerField(blank=True, null=True)
    quav_saba = models.IntegerField(blank=True, null=True)
    quav_domi = models.IntegerField(blank=True, null=True)
    quav_feri = models.IntegerField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valetransporte'


class Xmlesocial(models.Model):
    id = models.AutoField(primary_key=True)
    registro = models.CharField(max_length=14, blank=True, null=True)
    xml_empr = models.IntegerField(blank=True, null=True)
    xml_data = models.DateField(blank=True, null=True)
    xml_tipo = models.CharField(max_length=20, blank=True, null=True)
    xml_envi = models.TextField(blank=True, null=True)
    xml_reto = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xmlesocial'

