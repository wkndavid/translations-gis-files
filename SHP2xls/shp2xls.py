import geopandas as gpd

#caminho para o shapefile (.shp) local
caminho_shapefile = '/var/www/today/translations-esri-arcgis-files/SHP2xls/teste.shp'

#lê o shapefile para um GeoDataFrame ajustando a codificação
try:
    gdf = gpd.read_file(caminho_shapefile, encoding='utf-8')
except UnicodeDecodeError:
    try:
        gdf = gpd.read_file(caminho_shapefile, encoding='utf-16')
    except UnicodeDecodeError:
        gdf = gpd.read_file(caminho_shapefile, encoding='latin-1')

#caminho para salvar o arquivo Excel localmente (com a extensão .xlsx)
caminho_excel = '/var/www/today/translations-esri-arcgis-files/SHP2xls/results/result_shp2xls.xlsx'

#remove a coluna de geometria temporariamente para evitar erros
gdf_temp = gdf.copy()
del gdf_temp['geometry']

#salva o GeoDataFrame como um arquivo Excel usando o Pandas
gdf_temp.to_excel(caminho_excel, index=False, engine='openpyxl', encoding='utf-8')


    