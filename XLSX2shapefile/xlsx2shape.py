import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

#caminho para o arquivo Excel (.xls .xlsx) local
caminho_excel = '/var/www/today/translations-esri-arcgis-files/XLSX2shapefile/xlsx-testSHP.xlsx'

#ler dados do Excel para um DataFrame do pandas
dados_excel = pd.read_excel(caminho_excel)

print(dados_excel)

#adicionar uma geometria de ponto fictícia
geometry = [Point(0, 0) for _ in range(len(dados_excel))]
gdf = gpd.GeoDataFrame(dados_excel, geometry=geometry, crs='EPSG:4326')

#caminho para salvar o shapefile localmente (com a extensão .shp)
caminho_shapefile = '/var/www/today/translations-esri-arcgis-files/XLSX2shapefile/results/result_xlsx2shape.shp'

#saivarOGeoDataFramee como shapefile usando o GeoPandas
gdf.to_file(caminho_shapefile, driver='ESRI Shapefile')