# Mapeamento de campos por aba — badge de erro no tab header
# ---------------------------------------------------------------------------
 
ABA_CAMPOS = {
    "identificacao": [
        "func_empr", "func_fili", "func_codi", "func_regi", "func_nome",
        "func_sexo", "func_dana", "func_cpf", "func_pis", "func_esci",
        "func_naci", "func_raca", "func_vinc", "func_natu", "func_uf_natu",
        "func_pais_nasc", "func_pais_naci", "func_emai", "func_celu",
        "func_fone_dive", "func_inat", "func_apre",
    ],
    "endereco": [
        "func_tipo_logr", "func_ende", "func_bair", "func_cep",
        "func_esta", "func_ibge", "func_loca", "func_loca_uf",
    ],
    "vinculo": [
        "func_depa", "func_seto", "func_carg", "func_catr", "func_daad",
        "func_tiad", "func_demi", "func_tide", "func_fopa", "func_tisa",
        "func_tisa_rais", "func_cbo", "func_grin", "func_cose", "func_sind",
        "func_func_sind", "func_refe_desc_sind", "func_tipo_cont",
        "func_data_term_cont", "func_esoc_tipo_admi", "func_esoc_indi_admi",
        "func_natu_ativ", "func_cate_esoc", "func_cate_sefi", "func_ocor_sefi",
        "func_matr", "func_norm", "func_jorn", "func_esoc_regi_jorn",
        "func_regi_prev", "func_apos", "func_tp_rein", "func_num_proc",
        "func_lei_anis", "func_data_efet_reto", "func_data_efeito", "func_indi_contr",
    ],
    "salario": [
        "func_home", "func_hose", "func_same", "func_saho", "func_sala_cont",
        "func_valo_diar", "func_pens", "func_adqu", "func_insa", "func_peri",
        "func_perc_insa", "func_insa_sobr", "func_insa_sobr_valo", "func_base_insa",
        "func_alva", "func_vale_alim", "func_vale_trans",
        "func_remu_outr_tpinsc", "func_remu_outr_nrinsc", "func_remu_outr_cate",
        "func_remu_outr_valo", "func_remu_outr_indi",
    ],
    "banco": [
        "func_banc_paga", "func_agen", "func_cont_paga", "func_tipo_cred",
        "func_cont_fgts", "func_daop_fgts", "func_inss", "func_fgts", "func_irrf",
        "func_cons_fgts_inst", "func_cons_fgts_contr", "func_cons_fgts_even",
    ],
    "documentos": [
        "func_ctps", "func_seri_ctps", "func_esta_ctps", "func_emis_ctps",
        "func_titu", "func_digi_titu", "func_zona_titu", "func_seca_titu",
        "func_regi_prof", "func_regi_cate", "func_regi_vali",
        "func_rege", "func_rege_orga", "func_rege_expe", "func_rege_uf",
        "func_cnh", "func_cate", "func_cnh_prim", "func_cnh_emis",
        "func_cnh_vali", "func_cnh_esta", "func_rne", "func_rne_emis",
        "func_rne_expe", "func_extr_cond", "func_extr_data_cheg",
        "func_extr_casa_bras", "func_extr_filh_bras",
        "func_defi", "func_tipo_defi", "func_defi_cota",
    ],
    "jornada": [
        "func_en01", "func_sa01", "func_en02", "func_sa02",
        "func_saba", "func_domi", "func_feri",
        "func_dia1", "func_ven1", "func_dia2", "func_ven2", "func_temp_resi",
    ],
    "saude": [
        "func_venc_exam", "func_exam_data", "func_exam_codi", "func_exam_cnpj",
        "func_exam_crm", "func_exam_crm_uf", "func_data_expi_exam_ocup",
        "func_tipo_exam_ocup", "func_esta_natu_esta", "func_esta_nive_esta",
        "func_esta_data_term", "func_esta_inst_ensi",
        "func_apren_contr_dire", "func_apren_enti_qual",
    ],
    "esocial": [
        "func_esoc_tipo_insc", "func_esoc_nume_insc", "func_esoc_matr_ante",
        "func_codi_lota_trib", "func_cate_tpinsc", "func_cate_nrinsc",
        "func_esoc_data_tran", "func_esoc_tran_obse",
    ],
}
 
 
def _has_errors(form) -> dict:
    campos_com_erro = set(form.errors.keys())
    return {
        aba: bool(campos_com_erro & set(campos))
        for aba, campos in ABA_CAMPOS.items()
    }
 