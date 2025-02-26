# -*- coding: utf-8 -*-
import arcpy
import pandas as pd
import re
from dbfread import DBF
import json
import os

#definir o caminho do arquivo de log para o diretório do usuário
log_dir = os.path.expanduser('~')  # diretório do usuário
log_path = os.path.join(log_dir, 'traducao.log')

#configuração do log
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def carregar_dicionario(caminho_json):
    """carrega o dicionário de traduções a partir de um arquivo JSON."""
    try:
        arcpy.AddMessage("Carregando dicionário de traduções do arquivo JSON...")
        with open(caminho_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        mensagem = f"Erro de decodificação JSON: {str(e)}"
        arcpy.AddError(mensagem)
        raise
    except FileNotFoundError as e:
        mensagem = f"Arquivo JSON não encontrado: {str(e)}"
        arcpy.AddError(mensagem)
        raise
    except Exception as e:
        mensagem = f"Erro ao carregar o dicionário de traduções: {str(e)}"
        arcpy.AddError(mensagem)
        raise

def preprocessar_dicionario(traducoes):
    """preprocessa o dicionário para acrônimos."""
    arcpy.AddMessage("Preprocessando dicionário para acrônimos...")
    return {palavra.upper() for palavra in traducoes.keys()}

def traduzir_celulas(registro, acronimos, traducoes):
    """traduz as células de um registro usando o dicionário de traduções."""
    novo_registro = {}
    for coluna, valor in registro.items():
        if valor is None:
            novo_registro[coluna] = ''
            continue

        palavras = re.findall(r'\b\w+\b', str(valor))
        novo_registro[coluna] = ' '.join(
            traducoes.get(palavra.upper(), palavra) if palavra.upper() in acronimos else palavra
            for palavra in palavras
        )
    return novo_registro

def traduzir_dbf_e_salvar(dbf_path, output_path, acronimos, traducoes):
    """lê um arquivo DBF, traduz e salva como Excel."""
    try:
        arcpy.AddMessage("Iniciando o processamento do arquivo DBF...")
        table = DBF(dbf_path, encoding='latin1')

        arcpy.AddMessage("Traduzindo registros do arquivo DBF...")
        registros_traduzidos = [traduzir_celulas(registro, acronimos, traducoes) for registro in table]

        arcpy.AddMessage("Convertendo registros traduzidos para DataFrame...")
        df = pd.DataFrame(registros_traduzidos)

        arcpy.AddMessage("Salvando DataFrame como arquivo Excel...")
        df.to_excel(output_path, index=False, engine='openpyxl')

        mensagem = "Arquivo DBF traduzido e salvo com sucesso como arquivo Excel."
        arcpy.AddMessage(mensagem)
    except Exception as e:
        mensagem = f"Erro ao processar o arquivo DBF: {str(e)}"
        arcpy.AddError(mensagem)
        raise

def main():
    """função principal que executa o processamento do arquivo."""
    try:
        #obtendo parâmetros do ArcGIS Pro
        caminho_json = arcpy.GetParameterAsText(0)  # caminho para o arquivo JSON
        caminho_dbf = arcpy.GetParameterAsText(1)  # caminho para o arquivo DBF
        caminho_output_dbf = arcpy.GetParameterAsText(2)  # caminho de saída para o arquivo Excel

        #validar parâmetros
        if not arcpy.Exists(caminho_json):
            arcpy.AddError(f"O arquivo JSON especificado não existe: {caminho_json}")
            return
        if not arcpy.Exists(caminho_dbf):
            arcpy.AddError(f"O arquivo DBF especificado não existe: {caminho_dbf}")
            return

        #carrega o dicionário de traduções do arquivo JSON
        arcpy.AddMessage("Iniciando o carregamento do dicionário de traduções...")
        traducoes = carregar_dicionario(caminho_json)

        #preprocessa o dicionário para acrônimos
        acr_preprocessados = preprocessar_dicionario(traducoes)

        #executa as funções para traduzir o DBF e salvar como Excel
        arcpy.AddMessage("Iniciando a tradução do arquivo DBF e salvamento como Excel...")
        traduzir_dbf_e_salvar(caminho_dbf, caminho_output_dbf, acr_preprocessados, traducoes)
    
    except Exception as e:
        arcpy.AddError(f"Erro ao executar o script: {str(e)}")

if __name__ == "__main__":
    main()