from funcoes import leitura_csv, tratamento, extrair_valores, calcular_mediana,validacao_hipotese_pedidos
import csv

# 1. CAMINHOS DOS ARQUIVOS NA PASTA DATA
caminho_produtos = 'data/olist_products_dataset.csv'
caminho_produtos_tratados = 'data/olist_orders_products_limpo.csv'
caminho_pedidos = 'data/olist_orders_dataset.csv'

print("Extraindo e calculando a mediana ....")
lista_pesos = extrair_valores(caminho_produtos, 'product_weight_g')
mediana_peso = calcular_mediana(lista_pesos)
lista_comprimento = extrair_valores(caminho_produtos, 'product_length_cm')
mediana_comprimento = calcular_mediana(lista_comprimento)
lista_altura = extrair_valores(caminho_produtos, 'product_height_cm')
mediana_altura = calcular_mediana(lista_altura)
lista_largura = extrair_valores(caminho_produtos, 'product_width_cm')
mediana_largura = calcular_mediana(lista_largura)

# 2. REALIZAÇÃO DO TRATAMENTO
print("Realizando o tratamento de dados nulos e vazios...")
tratamento(caminho_produtos, caminho_produtos_tratados, mediana_peso, mediana_comprimento, mediana_altura, mediana_largura)

# 3. LEITURA DOS DADOS PARA A MEMÓRIA
print("Carregando os dados na memória....")
produtos = leitura_csv(caminho_produtos_tratados)
pedidos = leitura_csv(caminho_pedidos)

print(f"{len(produtos)} produtos e {len(pedidos)} pedidos carregados.")


# 4. Validar Hipótese de Pedidos
validacao_hipotese_pedidos(caminho_pedidos)

# --- TESTE DE LÓGICA DA MEDIANA ---
print(f"Teste Ímpar (deve ser 20): {calcular_mediana([10, 50, 20])}")
print(f"Teste Par (deve ser 25.0): {calcular_mediana([10, 20, 30, 40])}")
print("-" * 30)

# --- BLOCO DE AUDITORIA ---
print("\nAuditando o arquivo limpo...")
nulos_categoria = 0
nulos_peso = 0

with open(caminho_produtos_tratados, mode='r', encoding='utf-8') as arquivo_validacao:
    leitor_validacao = csv.DictReader(arquivo_validacao)
    for linha in leitor_validacao:
        if not linha['product_category_name'] or linha['product_category_name'].strip() == '':
            nulos_categoria += 1
        if not linha['product_weight_g'] or linha['product_weight_g'].strip() == '':
            nulos_peso += 1

print(f"-> Valores nulos restantes em 'product_category_name': {nulos_categoria}")
print(f"-> Valores nulos restantes em 'product_weight_g': {nulos_peso}")