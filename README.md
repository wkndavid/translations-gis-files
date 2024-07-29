# translations-esri-arcgis-files
#
# Descrição das Funções
carregar_dicionario(caminho_json)

# Parâmetros: 

traducoes: Dicionário de traduções.
Descrição: Pré-processa o dicionário para extrair e armazenar os acrônimos em maiúsculas.
traduzir_celulas(registro, acronimos, traducoes)
Parâmetros:
registro: Um registro do arquivo DBF.
acronimos: Conjunto de acrônimos extraídos do dicionário de traduções.
traducoes: Dicionário de traduções.
Descrição: Traduz as células do registro conforme o dicionário de traduções.
traduzir_dbf_e_salvar(dbf_path, output_path, acronimos, traducoes)
Parâmetros:
dbf_path: Caminho para o arquivo DBF de entrada.
output_path: Caminho para o arquivo Excel de saída.
acronimos: Conjunto de acrônimos extraídos do dicionário de traduções.
traducoes: Dicionário de traduções.
Descrição: Lê o arquivo DBF, traduz os registros e salva o resultado em um arquivo Excel.
Tratamento de Erros: Captura e registra erros durante o processamento do arquivo DBF, exibindo mensagens de erro e interrompendo a execução em caso de falhas críticas.

# Descrição Geral
Este script Python realiza a tradução de conteúdo em arquivos DBF, utilizando um dicionário de traduções fornecido em um arquivo JSON. O script lê os registros do arquivo DBF, traduz os textos conforme o dicionário e salva os resultados em um arquivo Excel. Além disso, o script faz uso de logging para registrar o progresso e possíveis erros durante a execução.


# Estrutura do Script

Estrutura do Script

Importações de Bibliotecas:

pandas: Utilizada para manipulação e exportação de dados em formato Excel.
re: Usada para operações de expressões regulares.
dbfread: Utilizada para leitura de arquivos DBF.
logging: Usada para registrar logs de eventos e erros.
json: Utilizada para manipulação de arquivos JSON.
art: Utilizada para criar arte ASCII para melhorar a visualização do progresso.

# Configuração do Logging:
-> Configura o logging para registrar informações em um arquivo chamado traducao.log.

# Funções Principais:

Configuração do Logging:

Configura o logging para registrar informações em um arquivo chamado traducao.log.

carregar_dicionario(caminho_json): Carrega o dicionário de traduções a partir de um arquivo JSON.
preprocessar_dicionario(traducoes): Pré-processa o dicionário para armazenar os acrônimos em maiúsculas.
traduzir_celulas(registro, acronimos, traducoes): Traduz as células do registro conforme o dicionário de traduções.
traduzir_dbf_e_salvar(dbf_path, output_path, acronimos, traducoes): Lê o arquivo DBF, traduz os registros e salva o resultado em um arquivo Excel.


# Configuração e Execução
Carregar o Dicionário de Traduções
-> O caminho para o arquivo JSON contendo o dicionário de traduções é definido pela variável caminho_json.

Pré-processar o Dicionário:

-> O dicionário de traduções é pré-processado para extrair e armazenar os acrônimos em maiúsculas.

# Traduzir e Salvar o Arquivo DBF:
-> O caminho do arquivo DBF de entrada e o caminho do arquivo Excel de saída são definidos.
-> A função traduzir_dbf_e_salvar é chamada para executar o processo de tradução e salvar o resultado.

#
![Build Status](https://img.shields.io/github/actions/workflow/status/wkndavid/translations-esri-arcgis-files/python-package.yml?branch=main)
![Coverage](https://img.shields.io/codecov/c/github/wkndavid/translations-esri-arcgis-files?branch=main)
[![Python package](https://github.com/wkndavid/translations-esri-arcgis-files/actions/workflows/python-package.yml/badge.svg)](https://github.com/wkndavid/translations-esri-arcgis-files/actions/workflows/python-package.yml)