import pandas as pd
from dbfread import DBF

def converter_dbf_para_csv(caminho_dbf, caminho_csv, encoding='latin-1'):
    try:
        # Ler o arquivo DBF
        dbf = DBF(caminho_dbf, encoding=encoding)
        
        # Converter para um DataFrame do pandas
        df = pd.DataFrame(iter(dbf))
        
        # Salvar o DataFrame como um arquivo CSV
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        print(f"Arquivo convertido para CSV com sucesso: {caminho_csv}")
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

# Caminho dos arquivos
caminho_dbf = '/var/www/today/translations-gis-files/DBF2csv/lotes_registrados.dbf'
caminho_csv = '/var/www/today/translations-gis-files/DBF2csv/deubom.csv'

# Converter o arquivo DBF para CSV
converter_dbf_para_csv(caminho_dbf, caminho_csv)
