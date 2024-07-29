import pandas as pd
import re
from dbfread import DBF
import logging
import json
from art import tprint

#configurando o logging
logging.basicConfig(filename='traducao.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#função para carregar o dicionário de traduções de um arquivo JSON
def carregar_dicionario(caminho_json):
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            traducoes = json.load(f)
        return traducoes
    except json.JSONDecodeError as e:
        logging.error(f"Erro de decodificação JSON: {str(e)}")
        raise
    except FileNotFoundError as e:
        logging.error(f"Arquivo JSON não encontrado: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Erro ao carregar o dicionário de traduções: {str(e)}")
        raise

#função para pré-processar o dicionário e armazenar os acrônimos
def preprocessar_dicionario(traducoes):
    acronimos = {palavra.upper() for palavra in traducoes.keys()}
    return acronimos

#função para traduzir as células
def traduzir_celulas(registro, acronimos, traducoes):
    novo_registro = {}
    for coluna, valor in registro.items():
        if valor is None:
            novo_registro[coluna] = ''
            continue

        novo_valor = []
        palavras = re.findall(r'\b\w+\b', str(valor))
        for palavra in palavras:
            palavra_upper = palavra.upper()
            if palavra_upper in acronimos:
                traduzida = traducoes.get(palavra_upper, palavra)
                novo_valor.append(traduzida)
            else:
                novo_valor.append(palavra)
        novo_registro[coluna] = ' '.join(novo_valor)
    return novo_registro

#função para ler um arquivo DBF, traduzir e salvar
def traduzir_dbf_e_salvar(dbf_path, output_path, acronimos, traducoes):
    try:
        tprint("Início do Processamento", font="block")  #título principal usando fonte "block"
        table = DBF(dbf_path, encoding='latin1')

        registros_traduzidos = []
        total_registros = len(table)
        for i, registro in enumerate(table):
            registros_traduzidos.append(traduzir_celulas(registro, acronimos, traducoes))
            if (i + 1) % 10 == 0 or i == total_registros - 1:
                print(f"Traduzindo registros: {i + 1}/{total_registros}")

        print("Convertendo para DataFrame...")
        df = pd.DataFrame(registros_traduzidos)

        print("Salvando em Excel...")
        df.to_excel(output_path, index=False, engine='openpyxl', encoding='latin1')

        logging.info("Arquivo DBF traduzido e salvo com sucesso")
        tprint("Processo Concluído", font="block")  #título principal usando fonte "block"
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo DBF: {str(e)}")
        print(f"Erro ao processar o arquivo DBF: {str(e)}")
        raise

#caminho para o arquivo JSON com o dicionário de traduções (minificado)
caminho_json = '/var/www/today/translations-esri-arcgis-files/DBFtranslation/traducao_minify.json'

#carrega o dicionário de traduções do arquivo JSON
traducoes = carregar_dicionario(caminho_json)

#caminho para o arquivo DBF de entrada
caminho_dbf = '/var/www/today/translations-esri-arcgis-files/DBFtranslation/dbf-xlsx2shape.dbf'

#caminho de saída para o arquivo Excel
caminho_output_dbf = '/var/www/today/translations-esri-arcgis-files/DBFtranslation//results/01today.xlsx'

#execute as funções para traduzir o DBF e salvar como Excel
acr_preprocessados = preprocessar_dicionario(traducoes)
traduzir_dbf_e_salvar(caminho_dbf, caminho_output_dbf, acr_preprocessados, traducoes)