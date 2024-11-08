import os
import random
from random import randint
from dotenv import load_dotenv
from fiscaliza.main import Fiscaliza
from fiscaliza.constants import MUNICIPIOS, SERVICOS
from fiscaliza.attrs import FIELDS

load_dotenv(override=True)

issue_id = "124176"
fiscaliza = Fiscaliza(os.environ["USERNAME"], os.environ["PASSWORD"], teste=True)
issue = fiscaliza.get_issue(issue_id)

# | code-fold: true
dados = {
    "endereco_da_inspecao": "Rua Machado de Assis, 27 - Morro Grande, Rio de Janeiro - RJ",
    "campo_eletrico__pico_vm": randint(50, 100),
    "campo_eletrico_rms_vm": randint(20, 100),
    "coordenacao_responsavel": "FI2",
    "cnpjcpf_da_entidade": "27865757000102",
    "entidade_com_cadastro_stel": "Sim",
    "entidade_da_inspecao": ["01109184000195", "27865757000102"],
    "entidade_outorgada": random.choice(["0", "1"]),
    "esta_em_operacao": randint(0, 1),
    "numero_da_estacao": "1493671",
    "fiscais": ["Eric Magalhães Delgado", "Ronaldo da Silva Alves Batista"],
    "fiscal_responsavel": "Eric Magalhães Delgado",
    "foi_constatada_interferencia": randint(0, 1),
    "frequencia_inicial": randint(70, 110),
    "frequencia_final": randint(110, 117),
    "gerar_relatorio": "1",
    "gerar_plai": 1,
    "tipo_do_processo_plai": random.choice(FIELDS["tipo_do_processo_plai"].options),
    "coord_fi_plai": random.choice(FIELDS["coord_fi_plai"].options),
    "html_path": "/mnt/c/Users/rsilva/code/fiscaliza/tests/Report_2024.02.18_T11.30.55_123456.html",
    "uploads": [
        {
            "path": "/mnt/c/Users/rsilva/code/fiscaliza/tests/Report_2024.02.18_T11.30.55_123456.json",
            "filename": "Info.json",
        }
    ],
    "identificada_a_origem": str(randint(0, 1)),
    "unidade_da_frequencia_final": "MHz",
    "unidade_da_frequencia_inicial": "MHz",
    "horas_de_conclusao": randint(1, 8),
    "horas_de_deslocamento": randint(1, 8),
    "horas_de_execucao": randint(8, 40),
    "horas_de_preparacao": randint(1, 8),
    "houve_obice": random.randint(0, 1),
    "houve_interferencia": random.choice(["Sim", "Não"]),
    "latitude_coordenadas": -randint(0, 33),
    "longitude_coordenadas": -randint(34, 73),
    "latitude_da_estacao": -randint(0, 33),
    "longitude_da_estacao": -randint(34, 73),
    "nome_da_entidade": "Globo S/A",
    "numero_do_pai": "123456",
    "observacao_tecnica_amostral": "Simulação com o HTZ",
    "pai_instaurado_pela_anatel": random.choice(["Sim", "Não"]),
    "precisa_reservar_instrumentos": "0",  #
    "procedimentos": random.choices(FIELDS["procedimentos"].options[1:], k=2),  #
    "qnt_produt_lacradosapreend": "0",
    "reserva_de_instrumentos": "0",
    "no_sav": "Teste de Quebra\n de linha",
    "documento_instaurador_do_pado": "0201235\n0201239\n0201237",
    "no_do_lacre": "50",
    "motivo_de_lai": random.choice(FIELDS["motivo_de_lai"].options),
    "no_sei_do_aviso_lai": "",
    "sanada_ou_mitigada": random.choice(["0", "1"]),
    "servicos_da_inspecao": random.choices(list(SERVICOS.values()), k=2),
    "situacao_constatada": "Irregular",
    "situacao_de_risco_a_vida": "Sim",
    "tipo_de_inspecao": "Uso do Espectro - Monitoração",
    "ufmunicipio": random.choices(MUNICIPIOS, k=2),
    "uso_de_produto_homologado": random.choice(["0", "1"]),
    "utilizou_algum_instrumento": "0",
    "utilizou_apoio_policial": random.choice(
        FIELDS["utilizou_apoio_policial"].options[1:]
    ),
    "utilizou_tecnicas_amostrais": random.choice(
        FIELDS["utilizou_tecnicas_amostrais"].options
    ),
    "description": "[PMEC 2024 Etapa 2] Monitorar canais e faixas de frequências relacionados às aplicações críticas (como, por exemplo, radionavegação e radiocomunicação aeronáutica e canais de emergência) na forma a ser estabelecida no Plano de Ação de Fiscalização.\r\n",
    "start_date": "2024-03-01",
    "due_date": "2024-05-30",
}

for tipo in FIELDS["tipo_de_inspecao"].options[1:]:
    dados["tipo_de_inspecao"] = tipo
    issue.update(dados)
