import geopandas as gpd
import subprocess
import os
import chardet

#caminho para o shapefile (.shp) local
caminho_shapefile = '/var/www/today/translations-esri-arcgis-files/SHP2xls/concessao.shp'
diretorio_shapefile = os.path.dirname(caminho_shapefile)
nome_base = os.path.splitext(os.path.basename(caminho_shapefile))[0]

#função para identificar a codificação de um arquivo
def identificar_codificacao(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'rb') as file:
            raw_data = file.read(10000)  #lê os primeiros 10.000 bytes do arquivo
        result = chardet.detect(raw_data)  #usa chardet para detectar a codificação
        return result['encoding']
    except Exception as e:
        print(f"Erro ao identificar a codificação: {e}")
        return None

#função para verificar e criar o arquivo .shx se necessário
def verificar_e_criar_shx(caminho_shapefile):
    shx_path = os.path.join(diretorio_shapefile, nome_base + '.shx')
    
    if not os.path.isfile(shx_path):
        print("Arquivo .shx não encontrado. Tentando criar...")
        try:
            comando = [
                'ogr2ogr', 
                '-f', 'ESRI Shapefile', 
                '-update', 
                '-append', 
                caminho_shapefile, 
                caminho_shapefile
            ]
            subprocess.run(comando, check=True)
            print("Arquivo .shx criado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao criar o arquivo .shx: {e}")
            exit(1)

#verifica e cria o arquivo .shx se necessário
verificar_e_criar_shx(caminho_shapefile)

#função para ler o shapefile ajustando a codificação
def ler_shapefile(caminho, encoding):
    try:
        print(f"Tentando ler o shapefile com codificação {encoding}")
        gdf = gpd.read_file(caminho, encoding=encoding)
        if not gdf.empty:
            print("Shapefile lido com sucesso.")
            return gdf
        else:
            print(f"O shapefile está vazio com codificação {encoding}.")
            return None
    except UnicodeDecodeError:
        print(f"Erro de codificação com {encoding}, tentando outra codificação.")
        return None

#identifica a codificação do arquivo .dbf associado ao shapefile
caminho_dbf = os.path.splitext(caminho_shapefile)[0] + '.dbf'
codificacao = identificar_codificacao(caminho_dbf)

if not codificacao:
    print("Não foi possível identificar a codificação. Verifique o arquivo.")
    exit(1)

#lê o shapefile com a codificação identificada
gdf = ler_shapefile(caminho_shapefile, codificacao)
if gdf is None or gdf.empty:
    print("Não foi possível ler o shapefile ou o GeoDataFrame está vazio.")
    exit(1)

#caminho para salvar o arquivo Excel localmente (com a extensão .xlsx)
caminho_excel = '/var/www/today/translations-esri-arcgis-files/SHP2xls/results/result_shp2xls.xlsx'

#remove a coluna de geometria temporariamente para evitar erros
gdf_temp = gdf.copy()
if 'geometry' in gdf_temp.columns:
    del gdf_temp['geometry']

#salva o GeoDataFrame como um arquivo Excel usando o Pandas
try:
    gdf_temp.to_excel(caminho_excel, index=False, engine='openpyxl', encoding='utf-8')
    print(f"Arquivo Excel salvo com sucesso em: {caminho_excel}")
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")
 