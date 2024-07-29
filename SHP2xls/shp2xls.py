import geopandas as gpd
import subprocess
import os

#caminho para o shapefile (.shp) local
caminho_shapefile = '/var/www/today/translations-esri-arcgis-files/SHP2xls/result_xlsx2shape.shp'
diretorio_shapefile = os.path.dirname(caminho_shapefile)
nome_base = os.path.splitext(os.path.basename(caminho_shapefile))[0]

#função para verificar e criar o arquivo .shx se necessário
def verificar_e_criar_shx(caminho_shapefile):
    shx_path = os.path.join(diretorio_shapefile, nome_base + '.shx')
    
    #verifica se o arquivo .shx existe
    if not os.path.isfile(shx_path):
        print("Arquivo .shx não encontrado. Tentando criar...")
        try:
            #usa ogr2ogr para criar o arquivo .shx
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
def ler_shapefile(caminho):
    encodings = [
        'utf-8', 'utf-16', 'latin-1', 'iso-8859-1', 'ascii', 'utf-32', 
        'cp1252', 'big5', 'gbk', 'shift_jis', 'euc-jp', 'euc-kr'
    ]
    for enc in encodings:
        try:
            print(f"Tentando ler o shapefile com codificação {enc}")
            gdf = gpd.read_file(caminho, encoding=enc)
            if not gdf.empty:
                print("Shapefile lido com sucesso.")
                return gdf
            else:
                print(f"O shapefile está vazio com codificação {enc}.")
        except (UnicodeDecodeError, ValueError) as e:
            print(f"Erro com codificação {enc}: {e}, tentando outra codificação.")
            continue
    raise ValueError("Não foi possível ler o shapefile com as codificações fornecidas.")

try:
    gdf = ler_shapefile(caminho_shapefile)
except Exception as e:
    print(f"Erro ao ler o shapefile: {e}")
    exit(1)

#verifica se o GeoDataFrame contém dados
if gdf.empty:
    print("O GeoDataFrame está vazio.")
else:
    print(f"GeoDataFrame contém {len(gdf)} registros.")

    #exibe alguns registros para diagnóstico
    print("Alguns registros do GeoDataFrame:")
    print(gdf.head())

#caminho para salvar o arquivo Excel localmente (com a extensão .xlsx)
caminho_excel = '/var/www/today/translations-esri-arcgis-files/SHP2xls/results/result_shp2xls.xlsx'

#remove a coluna de geometria temporariamente para evitar erros
gdf_temp = gdf.copy()
if 'geometry' in gdf_temp.columns:
    del gdf_temp['geometry']

#função para limpar caracteres inválidos
def limpar_dados(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            #exibe alguns dados antes da limpeza
            print(f"Dados da coluna {col} antes da limpeza:")
            print(df[col].head())

            df[col] = df[col].apply(lambda x: str(x).encode('utf-8', errors='ignore').decode('utf-8'))
            
            #exibe alguns dados após a limpeza
            print(f"Dados da coluna {col} após a limpeza:")
            print(df[col].head())
    return df

#limpa os dados antes de salvar
gdf_temp = limpar_dados(gdf_temp)

#salva o GeoDataFrame como um arquivo Excel usando o Pandas
try:
    gdf_temp.to_excel(caminho_excel, index=False, engine='openpyxl')
    print(f"Arquivo Excel salvo com sucesso em: {caminho_excel}")
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")
