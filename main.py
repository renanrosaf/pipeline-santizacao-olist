"""Pipeline de Sanitização de Dados - Olist
Arquivo principal (main) responsável por orquestrar a limpeza 
e validação das bases de dados de produtos e pedidos. Ele extrai medianas para 
tratamento de valores nulos, padroniza textos e datas, e gera um relatório final.
"""

#IMPORTACAO DAS FUNÇÕES E BIBLIOTECA NATIVA
from funcoes import leitura_csv, tratamento, extrair_valores, calcular_mediana,validacao_hipotese_pedidos,tratamento_pedidos,gerar_relatorio_final
import csv

# 1. CAMINHOS DOS ARQUIVOS NA PASTA DATA
caminho_produtos = 'data/olist_products_dataset.csv'
caminho_produtos_tratados = 'data/olist_orders_products_limpo.csv'
caminho_pedidos = 'data/olist_orders_dataset.csv'
caminho_pedidos_tratados='data/olist_orders_dataset_limpo.csv'

#2. REALIZAÇÃO DA REGRA DE CORTE (MEDIANA) E TRATAMENTOD A BASE DE PRODUTOS
print("Extraindo e calculando a mediana ....")
lista_pesos = extrair_valores(caminho_produtos, 'product_weight_g')
mediana_peso = calcular_mediana(lista_pesos)
lista_comprimento = extrair_valores(caminho_produtos, 'product_length_cm')
mediana_comprimento = calcular_mediana(lista_comprimento)
lista_altura = extrair_valores(caminho_produtos, 'product_height_cm')
mediana_altura = calcular_mediana(lista_altura)
lista_largura = extrair_valores(caminho_produtos, 'product_width_cm')
mediana_largura = calcular_mediana(lista_largura)

print("Realizando o tratamento de dados nulos e vazios...")

total_prod,nulos_prod=tratamento(
    caminho_produtos,caminho_produtos_tratados,
    mediana_peso,mediana_comprimento,mediana_altura,mediana_largura
)

#3. LEITURA DADOS PARA A MEMÓRIA:
print("Carregando os dados na memória...")
produtos=leitura_csv(caminho_produtos_tratados)
pedidos=leitura_csv(caminho_pedidos)
print(f"{len(produtos)} e {len(pedidos)} pedidos carregados")

# 4. REGRA DE NEGÓCIO E TRATAMENTO DA BASE DE PRODUTOS (VALIDAÇÃO E FORMATAÇÃO)
# Validação da hipótese de negócios sobre os pedidos cancelados
validacao_hipotese_pedidos(caminho_pedidos)

# Limpeza, descarte de nulos e conversão de datas para o padrão brasileiro
print("Conversão da data para o formato brasileiro...")
total_ped, cancelados_ped = tratamento_pedidos(caminho_pedidos, caminho_pedidos_tratados)

#6:RELATÓRIO DE STATUS:
linhas_totais = total_prod + total_ped
gerar_relatorio_final(linhas_totais, nulos_prod, cancelados_ped)

