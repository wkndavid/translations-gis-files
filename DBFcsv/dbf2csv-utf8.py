import pandas as pd

def converter_dbf_para_csv(caminho_dbf, caminho_csv, encoding='latin-1'):
    try:
        df = pd.read_csv(caminho_dbf, encoding=encoding)
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        print(f"Arquivo convertido para CSV com sucesso: {caminho_csv}")
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

# Use este script para converter seu arquivo .dbf
caminho_dbf = '/var/www/today/translations-esri-arcgis-files/DBFcsv/dbf2shape.dbf'
caminho_csv = '/var/www/today/translations-esri-arcgis-files/DBFcsv/dbf-xlsx2shape.csv'
converter_dbf_para_csv(caminho_dbf, caminho_csv)
