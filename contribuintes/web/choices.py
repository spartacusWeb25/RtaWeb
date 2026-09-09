LOGRADOURO_CHOICES = (
    ("", "Selecione"),
    (1, "Rua"),
    (2, "Avenida"),
    (3, "Travessa"),
    (4, "Beco"),
    (5, "Outros"),
)

TIPO_SANGUINEO_CHOICES = (
    ("", "Selecione"),
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)

ETNIA_RACA_CHOICES = (
    ("", "Selecione"),
    (0, "Excluído eSocial - Não informado"),
    (1, "Branca"),
    (2, "Preta"),
    (3, "Parda"),
    (4, "Amarela"),
    (5, "Indígena"),
)

SEXO_CHOICES = (
    ("", "Selecione"),
    (1, "Masculino"),
    (2, "Feminino"),
    (9, "Não informado"),
)

ESTADO_CIVIL_CHOICES = (
    ("", "Selecione"),
    (1, "Solteiro"),
    (2, "Casado"),
    (3, "Separado judicialmente"),
    (4, "Divorciado"),
    (5, "Viúvo"),
)

GRAU_INSTRUCAO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "Analfabeto"),
    (2, "Até 5ª série incompleta do EF"),
    (3, "5ª série completa do EF"),
    (4, "6ª a 9ª série do EF"),
    (5, "EF completo"),
    (6, "EM incompleto"),
    (7, "EM completo"),
    (8, "Superior incompleto"),
    (9, "Superior completo"),
    (10, "Pós-graduação"),
)

MOTIVO_DESLIGAMENTO_CHOICES = (
    ("", "Selecione"),
    (0, "Não se aplica"),
    (1, "Pedido de demissão"),
    (2, "Demissão por justa causa"),
    (3, "Demissão sem justa causa"),
    (99, "Outros"),
)

INDICATIVO_PENSAO_FGTS_CHOICES = (
    ("", "Selecione"),
    (0, "0 - Não existe pensão alimentícia"),
    (1, "1 - Existe pensão"),
    (2, "2 - Dedução de pensão"),
)

TEMPO_RESIDENCIA_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "Menos de 1 ano"),
    (2, "De 1 a 4 anos"),
    (3, "De 5 a 9 anos"),
    (4, "10 anos ou mais"),
)

CATEGORIA_CNH_CHOICES = (
    ("", "Selecione"),
    ("ACC", "ACC"),
    ("A",   "A"),
    ("B",   "B"),
    ("C",   "C"),
    ("D",   "D"),
    ("E",   "E"),
    ("AB",  "AB"),
    ("AC",  "AC"),
    ("AD",  "AD"),
    ("AE",  "AE"),
)

BANCOS_CHOICES = (
    ("", "Selecione"),
    ("001", "001 - Banco do Brasil"),
    ("033", "033 - Santander"),
    ("041", "041 - Banrisul"),
    ("070", "070 - BRB – Banco de Brasília"),
    ("077", "077 - Inter"),
    ("104", "104 - Caixa Econômica Federal"),
    ("136", "136 - Unicred"),
    ("197", "197 - Stone"),
    ("212", "212 - Banco Original"),
    ("237", "237 - Bradesco"),
    ("260", "260 - Nu Pagamentos (Nubank)"),
    ("290", "290 - PagSeguro"),
    ("318", "318 - Banco BMG"),
    ("336", "336 - C6 Bank"),
    ("341", "341 - Itaú Unibanco"),
    ("422", "422 - Safra"),
    ("623", "623 - Banco PAN"),
    ("633", "633 - Rendimento"),
    ("655", "655 - Votorantim"),
    ("707", "707 - Daycoval"),
    ("748", "748 - Sicredi"),
    ("756", "756 - Sicoob"),
)

VALID_BANCOS = {code for code, _ in BANCOS_CHOICES if code != ""}

CONDICAO_INGRESSO_CHOICES = (
    ("", "Selecione"),
    (0, "Não informado"),
    (1, "Residente"),
    (2, "Não residente"),
)

UF_CHOICES = (
    ("", "Selecione"),
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
)

ORDENACAO_CHOICES = (
    ("codigo_crescente", "Código crescente"),
    ("codigo_decrescente", "Código decrescente"),
    ("nome_crescente", "Nome crescente"),
    ("nome_decrescente", "Nome decrescente"),
)

CATEGORIA_SEFIP_CHOICES = (
    ("", "Selecione"),
    (1, "01 - Empregado"),
    (2, "02 - Trabalhador Avulso"),
    (3, "03 - Trabalhador não vinculado ao RGPS, mas com direito ao FGTS."),
    (4, "04 - Empregado sob contrato de trabalho por prazo determinado (Lei nº 9.601/98)."),
    (5, "05 - Contribuinte Individual - Diretor não empregado com FGTS (Lei nº 8.036/90, art.16)"),
    (6, "06 - Empregado Doméstico"),
    (7, "07 - Menor Aprendiz (Lei 10.097/2000)"),
    (11, "11 - Contribuinte Individual - Diretor não empregado e demais empresários sem FGTS."),
    (12, "12 - Demais Agentes Públicos"),
    (13, "13 - Contribuinte Individual - Trabalhador autônomo ou a este equiparado, inclusive o operador de máquina, com contribuição sobre remuneração cooperado que presta serviço a pessoas físicas, por intermédio da cooperativa de trabalho"),
)

CATEGORIA_ESOCIAL_CHOICES = (
    ("", "Selecione"),
    (101, "101 - Empregado - Geral, inclusive o empregado público da administração direta ou indireta contratado pela CLT"),
    (102, "102 - Empregado - Trabalhador rural por pequeno prazo da Lei 11.718/2008"),
    (103, "103 - Empregado - Aprendiz"),
    (104, "104 - Empregado - Doméstico"),
    (105, "105 - Empregado - Contrato a termo firmado nos termos da Lei 9.601/1998"),
    (106, "106 - Trabalhador temporário - Contrato nos termos da Lei 6.019/1974"),
    (107, "107 - Empregado - Contrato de trabalho Verde e Amarelo - sem acordo para antecipação mensal da multa rescisória do FGTS"),
    (108, "108 - Empregado - Contrato de trabalho Verde e Amarelo - com acordo para antecipação mensal da multa rescisória do FGTS"),
    (111, "111 - Empregado - Contrato de trabalho intermitente"),
    (201, "201 - Trabalhador avulso portuário"),
    (202, "202 - Trabalhador avulso não portuário"),
    (301, "301 - Servidor público titular de cargo efetivo, magistrado, ministro de Tribunal de Contas, conselheiro de Tribunal de Contas e membro do Ministério Público"),
    (302, "302 - Servidor público ocupante de cargo exclusivo em comissão"),
    (303, "303 - Exercente de mandato eletivo"),
    (304, "304 - Servidor público exercente de mandato eletivo, inclusive com exercício de cargo em comissão"),
    (305, "305 - Servidor público indicado para conselho ou órgão deliberativo, na condição de representante do governo, órgão ou entidade da administração pública"),
    (306, "306 - Servidor público contratado por tempo determinado, sujeito a regime administrativo especial definido em lei própria"),
    (307, "307 - Militar dos Estados e Distrito Federal"),
    (308, "308 - Conscrito"),
    (309, "309 - Agente público - Outros"),
    (310, "310 - Servidor público eventual"),
    (311, "311 - Ministros, juízes, procuradores, promotores ou oficiais de justiça à disposição da Justiça Eleitoral"),
    (312, "312 - Auxiliar local"),
    (313, "313 - Servidor público exercente de atividade de instrutoria, curso ou concurso, convocado para pareceres técnicos, depoimentos ou aditância no exterior"),
    (314, "314 - Militar das Forças Armadas"),
    (401, "401 - Dirigente sindical - Informação prestada pelo sindicato"),
    (410, "410 - Trabalhador cedido/exercício em outro órgão/juiz auxiliar - Informação prestada pelo cessionário/destino"),
    (501, "501 - Dirigente sindical - Segurado especial"),
    (701, "701 - Contribuinte individual - Autônomo em geral, exceto se enquadrado em uma das demais categorias de contribuinte individual"),
    (711, "711 - Contribuinte individual - Transportador autônomo de passageiros"),
    (712, "712 - Contribuinte individual - Transportador autônomo de carga"),
    (721, "721 - Contribuinte individual - Empresário, sócio e membro de conselho de administração ou fiscal com FGTS"),
    (722, "722 - Contribuinte individual - Diretor não empregado, sem FGTS"),
    (723, "723 - Contribuinte individual - Empresário, sócio e membro de conselho de administração ou fiscal"),
    (731, "731 - Contribuinte individual - Cooperado que presta serviços por intermédio de cooperativa de trabalho"),
    (734, "734 - Contribuinte individual - Transportador cooperado que presta serviços por intermédio de cooperativa de trabalho"),
    (738, "738 - Contribuinte individual - Cooperado filiado a cooperativa de produção"),
    (741, "741 - Contribuinte individual - Microempreendedor individual"),
    (751, "751 - Contribuinte individual - Magistrado classista temporário da Justiça do Trabalho ou da Justiça Eleitoral que seja aposentado de qualquer regime previdenciário"),
    (761, "761 - Contribuinte individual - Associado eleito para direção de cooperativa, associação ou entidade de classe de qualquer natureza ou finalidade, bem como o síndico ou administrador eleito para exercer atividade de direção condominial, desde que recebam remuneração"),
    (771, "771 - Contribuinte individual - Membro de conselho tutelar, nos termos da Lei 8.069/1990"),
    (781, "781 - Ministro de confissão religiosa ou membro de vida consagrada, de congregação ou de ordem religiosa"),
    (901, "901 - Estagiário"),
    (902, "902 - Médico residente, residente em área profissional de saúde ou médico em curso de formação"),
    (903, "903 - Bolsista"),
    (904, "904 - Participante de curso de formação, como etapa de concurso público, sem vínculo de emprego/estatutário"),
    (906, "906 - Beneficiário do Programa Nacional de Prestação de Serviço Civil Voluntário"),
)

GRAU_RISCO_CHOICES = (
    ("", "Selecione"),
    (0, "0 - Nunca exposto a agente nocivo"),
    (1, "1 - Grau 1 Leve - Não exposição a agente nocivo"),
    (2, "2 - Grau 2 Médio - Exposição a agente nocivo (aposentadoria especial aos 20 anos)"),
    (3, "3 - Grau 3 Grave - Exposição a agente nocivo (aposentadoria especial aos 15 anos)"),
    (4, "4 - Exposição a agente nocivo (aposentadoria especial aos 25 anos)"),
    (5, "5 - Não exposto a agente nocivo (mais de um vínculo)"),
    (6, "6 - Exposição a agente nocivo (15 anos) (mais de um vínculo)"),
    (7, "7 - Exposição a agente nocivo (20 anos) (mais de um vínculo)"),
)

REGIME_PREVIDENCIARIO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - RGPS - Regime Geral da Previdência Social"),
    (2, "2 - RPPS - Regime Próprio de Previdência Social (Servidor Público)"),
    (3, "3 - RPPE - Regime Próprio de Previdência Social no Exterior"),
    (9, "9 - Não informado"),
)

REGIME_TRABALHISTA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - CLT - Consolidação das Leis do Trabalho"),
    (2, "2 - Diretor Não Empregado"),
    (3, "3 - Estagiário"),
    (9, "9 - Outros"),
)

CLASSE_CONTRIBUINTE_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Mensalista"),
    (2, "2 - Prolaborista"),
    (3, "3 - Horista"),
    (9, "9 - Outros"),
)

TIPO_VINCULO_EMPREGATICIO_CHOICES = (
    ("", "Selecione"),
    (10, "10 - Trabalhador urbano vinculado a empregador pessoa jurídica por contrato de trabalho regido pela CLT, por prazo indeterminado."),
    (15, "15 - Trabalhador urbano vinculado a empregador pessoa física por contrato de trabalho regido pela CLT, por prazo indeterminado."),
    (20, "20 - Trabalhador rural vinculado a empregador pessoa jurídica por contrato de trabalho regido pela Lei nº 5.889/73, por prazo indeterminado."),
    (25, "25 - Trabalhador rural vinculado a empregador pessoa física por contrato de trabalho regido pela Lei nº 5.889/73, por prazo indeterminado."),
    (30, "30 - Servidor regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado ao Regime Próprio de Previdência."),
    (31, "31 - Servidor regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado ao Regime Geral de Previdência Social."),
    (35, "35 - Servidor público não-efetivo (demissível ad nutum)."),
    (40, "40 - Trabalhador avulso (trabalho administrado pelo sindicato da categoria ou pelo órgão gestor de mão-de-obra) para o qual é devido depósito de FGTS e ICF 88, art. 7º, inciso III."),
    (50, "50 - Trabalhador temporário, regido pela Lei nº 6.019, de 3 de janeiro de 1974."),
    (55, "55 - Aprendiz contratado na forma dos arts. 429 ou 430 da CLT, com redações dadas pela Lei nº 10.097, de 19 de dezembro de 2000."),
    (60, "60 - Trabalhador urbano vinculado a empregador pessoa jurídica por contrato de trabalho regido pela CLT, por tempo determinado ou obra certa."),
    (65, "65 - Trabalhador urbano vinculado a empregador pessoa física por contrato de trabalho regido pela CLT, por tempo determinado ou obra certa."),
    (70, "70 - Trabalhador rural vinculado a empregador pessoa jurídica por contrato de trabalho regido pela Lei nº 5.889/73, por prazo determinado."),
    (75, "75 - Trabalhador rural vinculado a empregador pessoa física por contrato de trabalho regido pela Lei nº 5.889/73, por prazo determinado."),
    (80, "80 - Diretor sem vínculo empregatício para o qual o empregador tenha optado pelo recolhimento do FGTS."),
    (90, "90 - Contrato de Trabalho por Prazo Determinado, regido pela Lei nº 9.601, de 21 de janeiro de 1998."),
    (95, "95 - Contrato de Trabalho por Tempo Determinado, regido pela Lei nº 8.745, de 9 de dezembro de 1993, com redação dada pela Lei nº 9.849, de 26 de outubro de 1999."),
    (96, "96 - Contrato de Trabalho por Prazo Determinado, regido por Lei Estadual."),
    (97, "97 - Contrato de Trabalho por Prazo Determinado, regido por Lei Municipal."),
)

NATUREZA_OCUPACAO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Empregado"),
    (2, "2 - Doméstico"),
    (3, "3 - Empregador-titular"),
    (4, "4 - Autônomo"),
    (5, "5 - Segurado Especial"),
    (9, "9 - Outros"),
)

FORMA_PAGAMENTO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Mensal"),
    (2, "2 - Quinzenal"),
    (3, "3 - Semanal"),
    (4, "4 - Diário"),
)

TIPO_CONTA_BANCARIA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Conta Corrente"),
    (2, "2 - Conta Poupança / Salário"),
    (3, "3 - Conta Pagamento"),
)

MODO_PAGAMENTO_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Depósito em Conta"),
    (2, "2 - Cheque"),
    (3, "3 - Dinheiro em Espécie"),
    (4, "4 - Cartão de Débito/Salário"),
)

TIPO_ORIGEM_CNPJ_CPF_CHOICES = (
    ("", "Selecione"),
    (1, "1 - CNPJ"),
    (2, "2 - CPF"),
)

TIPO_DEPENDENTE_CHOICES = (
    ("", "Selecione"),
    (1, "1 - Cônjuge / Companheiro(a)"),
    (2, "2 - Filho(a) / Menor sob guarda"),
    (3, "3 - Pai / Mãe"),
    (4, "4 - Outros parentes"),
)

TIPO_DEPENDENCIA_CHOICES = (
    ("", "Selecione"),
    (1, "1 - IRRF - Imposto de Renda"),
    (2, "2 - Salário Família"),
    (3, "3 - Pensão Alimentícia / Desconto Folha"),
    (4, "4 - Outros"),
)


ESOCIAL_COUNTRIES_MD = """| 008 | Abu Dhabi | - | 13/12/1996 |
| 009 | Dirce | - | 13/12/1996 |
| 013 | Afeganistao | - | |
| 017 | Albania, Republica Da | - | |
| 020 | Alboran-Perejil,Ilhas | - | 13/12/1996 |
| 023 | Alemanha | - | |
| 025 | Alemanha, Republica Democratica | - | 13/12/1996 |
| 031 | Burkina Faso | - | |
| 037 | Andorra | - | |
| 040 | Angola | - | |
| 041 | Anguilla | - | |
| 043 | Antigua E Barbuda | - | |
| 047 | Antilhas Holandesas | - | |
| 053 | Arabia Saudita | - | |
| 059 | Argelia | - | |
| 063 | Argentina | - | |
| 064 | Armenia, Republica Da | - | |
| 065 | Aruba | - | |
| 069 | Australia | - | |
| 072 | Austria | - | |
| 073 | Azerbaijao, Republica Do | - | |
| 077 | Bahamas, Ilhas | - | |
| 080 | Bahrein, Ilhas | - | |
| 081 | Bangladesh | - | |
| 083 | Barbados | - | |
| 085 | Belarus, Republica Da | - | |
| 087 | Belgica | - | |
| 088 | Belize | - | |
| 090 | Bermudas | - | |
| 093 | Mianmar (BIRMANIA) | - | |
| 097 | Bolivia, Estado Plurinacional Da | - | |
| 098 | Bosnia-Herzegovina (REPUBLICA Da) | - | |
| 100 | Int.Z.F.Manaus | 01/12/1991 | 13/12/1996 |
| 101 | Botsuana | - | |
| 105 | Brasil | - | |
| 106 | Fretado P/Brasil | 01/12/1991 | 14/11/1996 |
| 108 | Brunei | - | |
| 111 | Bulgaria, Republica Da | - | |
| 115 | Burundi | - | |
| 119 | Butao | - | |
| 127 | Cabo Verde, Republica De | - | |
| 131 | Cachemira | - | 13/12/1996 |
| 137 | Cayman, Ilhas | - | |
| 141 | Camboja | - | |
| 145 | Camaroes | - | |
| 149 | Canada | - | |
| 150 | Jersey, Ilha Do Canal | - | |
| 151 | Canarias, Ilhas | - | |
| 152 | Canal,Ilhas | - | 13/12/1996 |
| 153 | Cazaquistao, Republica Do | - | |
| 154 | Catar | - | |
| 158 | Chile | - | |
| 160 | China, Republica Popular | - | |
| 161 | Formosa (TAIWAN) | - | |
| 163 | Chipre | - | |
| 165 | Cocos(Keeling),Ilhas | - | |
| 169 | Colombia | - | |
| 173 | Comores, Ilhas | - | |
| 177 | Congo | - | |
| 183 | Cook, Ilhas | - | |
| 187 | Coreia (DO Norte),  Rep.Pop.Democratica | - | |
| 190 | Coreia (DO Sul), Republica Da | - | |
| 193 | Costa Do Marfim | - | |
| 195 | Croacia (REPUBLICA Da) | - | |
| 196 | Costa Rica | - | |
| 198 | Coveite | - | |
| 199 | Cuba | - | |
| 229 | Benin | - | |
| 232 | Dinamarca | - | |
| 235 | Dominica,Ilha | - | |
| 237 | Dubai | - | 13/12/1996 |
| 239 | Equador | - | |
| 240 | Egito | - | |
| 243 | Eritreia | 17/07/2006 | |
| 244 | Emirados Arabes Unidos | - | |
| 245 | Espanha | - | |
| 246 | Eslovenia, Republica Da | - | |
| 247 | Eslovaca, Republica | - | |
| 249 | Estados Unidos | - | |
| 251 | Estonia, Republica Da | - | |
| 253 | Etiopia | - | |
| 255 | Falkland (ILHAS Malvinas) | - | |
| 259 | Feroe, Ilhas | - | |
| 263 | Fezzan | - | 13/12/1996 |
| 267 | Filipinas | - | |
| 271 | Finlandia | - | |
| 275 | Franca | - | |
| 281 | Gabao | - | |
| 285 | Gambia | - | |
| 289 | Gana | - | |
| 291 | Georgia, Republica Da | - | |
| 293 | Gibraltar | - | |
| 297 | Granada | - | |
| 301 | Grecia | - | |
| 305 | Groenlandia | - | |
| 309 | Guadalupe | - | |
| 313 | Guam | - | |
| 317 | Guatemala | - | |
| 325 | Guiana Francesa | - | |
| 329 | Guine | - | |
| 331 | Guine-Equatorial | - | |
| 334 | Guine-Bissau | - | |
| 337 | Guiana | - | |
| 341 | Haiti | - | |
| 345 | Honduras | - | |
| 351 | Hong Kong | - | |
| 355 | Hungria, Republica Da | - | |
| 357 | Iemen | - | |
| 358 | Iemem Do Sul | - | 13/12/1996 |
| 359 | Man, Ilha De | - | |
| 361 | India | - | |
| 365 | Indonesia | - | |
| 367 | Inglaterra | - | 18/03/1997 |
| 369 | Iraque | - | |
| 372 | Ira, Republica Islamica Do | - | |
| 375 | Irlanda | - | |
| 379 | Islandia | - | |
| 383 | Israel | - | |
| 386 | Italia | - | |
| 388 | Servia E Montenegro | - | |
| 391 | Jamaica | - | |
| 395 | Jammu | - | 13/12/1996 |
| 396 | Johnston, Ilhas | - | |
| 399 | Japao | - | |
| 403 | Jordania | - | |
| 411 | Kiribati | - | |
| 420 | Laos, Rep.Pop.Democr.Do | - | |
| 423 | Lebuan,Ilhas | - | |
| 426 | Lesoto | - | |
| 427 | Letonia, Republica Da | - | |
| 431 | Libano | - | |
| 434 | Liberia | - | |
| 438 | Libia | - | |
| 440 | Liechtenstein | - | |
| 442 | Lituania, Republica Da | - | |
| 445 | Luxemburgo | - | |
| 447 | Macau | - | |
| 449 | Macedonia, Ant.Rep.Iugoslava | - | |
| 450 | Madagascar | - | |
| 452 | Ilha Da Madeira | - | |
| 455 | Malasia | - | |
| 458 | Malavi | - | |
| 461 | Maldivas | - | |
| 464 | Mali | - | |
| 467 | Malta | - | |
| 472 | Marianas Do Norte | - | |
| 474 | Marrocos | - | |
| 476 | Marshall,Ilhas | - | |
| 477 | Martinica | - | |
| 485 | Mauricio | - | |
| 488 | Mauritania | - | |
| 490 | Midway, Ilhas | - | |
| 493 | Mexico | - | |
| 494 | Moldavia, Republica Da | - | |
| 495 | Monaco | - | |
| 497 | Mongolia | - | |
| 499 | Micronesia | - | |
| 501 | Montserrat,Ilhas | - | |
| 505 | Mocambique | - | |
| 507 | Namibia | - | |
| 508 | Nauru | - | |
| 511 | Christmas,Ilha (NAVIDAD) | - | |
| 517 | Nepal | - | |
| 521 | Nicaragua | - | |
| 525 | Niger | - | |
| 528 | Nigeria | - | |
| 531 | Niue,Ilha | - | |
| 535 | Norfolk,Ilha | - | |
| 538 | Noruega | - | |
| 542 | Nova Caledonia | - | |
| 545 | Papua Nova Guine | - | |
| 548 | Nova Zelandia | - | |
| 551 | Vanuatu | - | |
| 556 | Oma | - | |
| 563 | Pacifico,Ilhas Do (ADMINISTRACAO Dos  Eua) | - | 13/12/1996 |
| 566 | Pacifico,Ilhas Do (POSSESSAO Dos Eua) | - | |
| 569 | Pacifico,Ilhas Do (TERRITORIO Em  Fideicomisso Dos | - | 13/12/1996 |
| 573 | Paises Baixos (HOLANDA) | - | |
| 575 | Palau | - | |
| 576 | Paquistao | - | |
| 578 | Palestina | 25/01/2011 | |
| 580 | Panama | - | |
| 583 | Papua Nova Guiné | 01/12/1991 | 13/12/1996 |
| 586 | Paraguai | - | |
| 589 | Peru | - | |
| 593 | Pitcairn,Ilha | - | |
| 599 | Polinesia Francesa | - | |
| 603 | Polonia, Republica Da | - | |
| 607 | Portugal | - | |
| 611 | Porto Rico | - | |
| 623 | Quenia | - | |
| 625 | Quirguiz, Republica | - | |
| 628 | Reino Unido | - | |
| 640 | Republica Centro-Africana | - | |
| 647 | Republica Dominicana | - | |
| 660 | Reuniao, Ilha | - | |
| 665 | Zimbabue | - | |
| 670 | Romenia | - | |
| 675 | Ruanda | - | |
| 676 | Russia, Federacao Da | - | |
| 677 | Salomao, Ilhas | - | |
| 678 | Saint Kitts E Nevis | - | |
| 685 | Saara Ocidental | - | |
| 687 | El Salvador | - | |
| 690 | Samoa | - | |
| 691 | Samoa Americana | - | |
| 695 | Sao Cristovao E Neves,Ilhas | - | |
| 697 | San Marino | - | |
| 700 | Sao Pedro E Miquelon | - | |
| 705 | Sao Vicente E Granadinas | - | |
| 710 | Santa Helena | - | |
| 715 | Santa Lucia | - | |
| 720 | Sao Tome E Principe, Ilhas | - | |
| 728 | Senegal | - | |
| 731 | Seychelles | - | |
| 735 | Serra Leoa | - | |
| 738 | Sikkim | - | 13/12/1996 |
| 741 | Cingapura | - | |
| 744 | Siria, Republica Arabe Da | - | |
| 748 | Somalia | - | |
| 750 | Sri Lanka | - | |
| 754 | Suazilandia | - | |
| 756 | Africa Do Sul | - | |
| 759 | Sudao | - | |
| 764 | Suecia | - | |
| 767 | Suica | - | |
| 770 | Suriname | - | |
| 772 | Tadjiquistao, Republica Do | - | |
| 776 | Tailandia | - | |
| 780 | Tanzania, Rep.Unida Da | - | |
| 782 | Territorio Brit.Oc.Indico | - | |
| 783 | Djibuti | - | |
| 785 | Territorio da Alta Comissao do  Pacifico Ocidental | - | 13/12/1996 |
| 788 | Chade | - | |
| 790 | Tchecoslovaquia | - | 13/12/1996 |
| 791 | Tcheca, Republica | - | |
| 795 | Timor Leste | - | |
| 800 | Togo | - | |
| 805 | Toquelau,Ilhas | - | |
| 810 | Tonga | - | |
| 815 | Trinidad E Tobago | - | |
| 820 | Tunisia | - | |
| 823 | Turcas E Caicos,Ilhas | - | |
| 824 | Turcomenistao, Republica Do | - | |
| 827 | Turquia | - | |
| 828 | Tuvalu | - | |
| 831 | Ucrania | - | |
| 833 | Uganda | - | |
| 840 | Uniao Das Republicas Socialistas  Sovieticas | - | 13/12/1996 |
| 845 | Uruguai | - | |
| 847 | Uzbequistao, Republica Do | - | |
| 848 | Vaticano, Est.Da Cidade Do | - | |
| 850 | Venezuela | - | |
| 855 | Vietname Norte | - | 13/12/1996 |
| 858 | Vietna | - | |
| 863 | Virgens,Ilhas (BRITANICAS) | - | |
| 866 | Virgens,Ilhas (E.U.A.) | - | |
| 870 | Fiji | - | |
| 873 | Wake, Ilha | - | |
| 875 | Wallis E Futuna, Ilhas | - | |
| 888 | Congo, Republica Democratica Do | - | |
| 890 | Zambia | - | |"""


def _build_country_choices():
    choices = [("", "Selecione")]
    for line in ESOCIAL_COUNTRIES_MD.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        code = parts[0]
        name = parts[1]
        if not str(code).strip().isdigit():
            continue
        code_int = int(code)
        code_str = str(code_int).zfill(3)
        choices.append((code_int, f"{code_str} - {name}"))
    return tuple(choices)


COUNTRY_CHOICES = _build_country_choices()

_TOP_CIDADES_IBGE = []
try:
    import pathlib as _pl
    _src = _pl.Path(r"dependentescontr/choices.py").read_text(encoding="utf-8")
    _start = _src.index("_TOP_CIDADES_IBGE = [")
    _end = _src.index("def _build_cidades_choices():", _start)
    _bloco = _src[_start:_end]
    exec(_bloco, globals())
except Exception:
    pass


def _build_cidades_choices():
    choices = [("", "Selecione a cidade...")]
    seen = set()
    for codigo, nome, uf in _TOP_CIDADES_IBGE:
        try:
            codigo_num = int(codigo)
        except Exception:
            continue
        if codigo_num in seen:
            continue
        seen.add(codigo_num)
        choices.append((codigo_num, f"{codigo:0>7} — {nome} / {uf}"))
    return choices


CIDADES_TOP_BR_CHOICES = _build_cidades_choices()

CIDADES_POR_CODIGO = {}
for codigo, nome, uf in _TOP_CIDADES_IBGE:
    try:
        codigo_num = int(codigo)
    except Exception:
        continue
    if codigo_num not in CIDADES_POR_CODIGO:
        CIDADES_POR_CODIGO[codigo_num] = (nome, uf)


PAISES_POR_CODIGO = {}
for valor, label in COUNTRY_CHOICES:
    if valor in (None, ""):
        continue
    try:
        PAISES_POR_CODIGO[int(valor)] = label
    except Exception:
        pass


def _choices_with_current(base_choices, value):
    choices = list(base_choices)
    if value in (None, ""):
        return tuple(choices)

    value_str = str(value).strip()
    valid_values = {str(choice_value) for choice_value, _ in choices if choice_value not in (None, "")}
    if value_str not in valid_values:
        try:
            original_value = value
            if isinstance(base_choices[0][0], int) and str(value).isdigit():
                original_value = int(value)
            choices.append((original_value, f"{value} - {value}"))
        except (ValueError, IndexError):
            choices.append((value, f"{value} - {value}"))
    return tuple(choices)


def _current_field_value(form, field_name):
    value = None
    if form.is_bound:
        value = form.data.get(field_name)
    if value in (None, ""):
        value = form.initial.get(field_name)
    if value in (None, "") and getattr(form.instance, "pk", None):
        value = getattr(form.instance, field_name, None)
    return value
