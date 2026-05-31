"""Módulo de Funções - Pipeline Olist
Este módulo contém todas as funções auxiliares utilizadas para a leitura, 
limpeza, validação e formatação das bases de dados de produtos e pedidos.
"""

# IMPORTAÇÃO DAS BIBLIOTECAS NATIVAS PYTHON
import csv
import re
from datetime import datetime


def limpar_texto(texto):
    """
    Limpa e padroniza o nome de uma categoria de produto.
    
    Aplica conversão para minúsculas, remoção de espaços e
    limpeza de caracteres especiais via Regex.
    
    Parâmetros:
        texto (str): Nome da categoria bruta.
    
    Retorna:
        str: Categoria padronizada ou "Sem categoria" se vazia.
    """
    # Verifica se a string é vazia ou o dado é nulo
    if not texto or texto.strip() == '':
        return "Sem categoria"

    texto_limpo = texto.lower()                          # converte para minúsculas
    texto_limpo = texto_limpo.strip()                    # remove espaços no início e fim
    texto_limpo = re.sub(r'[^\w\s]', "", texto_limpo)   # remove caracteres especiais

    # Proteção: se após o Regex a string ficou vazia
    if texto_limpo.strip() == '':
        return "Sem categoria"

    return texto_limpo


def formatar_data(data_string):
    """
    Converte uma data do formato ISO para o formato brasileiro.
    
    Parâmetros:
        data_string (str): Data no formato "AAAA-MM-DD HH:MM:SS".
    
    Retorna:
        str: Data no formato "DD/MM/AAAA" ou string vazia se nula.
    """
    # Verifica se a data está vazia ou nula antes de converter
    if not data_string or data_string.strip() == '':
        return ''
    try:
        # Converte string → objeto datetime
        data_obj = datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
        # Converte objeto datetime → formato brasileiro
        return data_obj.strftime('%d/%m/%Y')
    except ValueError:
        # Se o formato for inesperado, mantém o valor original
        return data_string


def leitura_csv(caminho):
    """
    Lê um arquivo CSV e retorna seu conteúdo como lista de dicionários.
    
    Parâmetros:
        caminho (str): Caminho para o arquivo CSV.
    
    Retorna:
        list: Lista de dicionários onde cada item é uma linha do CSV.
    """
    registros = []
    with open(caminho, mode='r', encoding='utf-8') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            registros.append(linha)
    return registros


def extrair_valores(caminho, nome_coluna):
    """
    Extrai os valores numéricos válidos de uma coluna do CSV.
    
    Ignora células vazias ou nulas.
    
    Parâmetros:
        caminho (str): Caminho para o arquivo CSV.
        nome_coluna (str): Nome da coluna a extrair.
    
    Retorna:
        list: Lista de floats com os valores válidos encontrados.
    """
    valores = []
    with open(caminho, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            dado_bruto = linha[nome_coluna]
            # Ignora células vazias ou nulas
            if dado_bruto and dado_bruto.strip() != '':
                valores.append(float(dado_bruto))
    return valores


def calcular_mediana(lista_valores):
    """
    Calcula a mediana de uma lista de valores numéricos.
    
    A mediana foi escolhida em vez da média pois o dataset da Olist
    contém produtos muito heterogêneos (de gramas a dezenas de quilos),
    criando outliers que distorceriam a média. A mediana representa
    o valor central sem ser influenciada por produtos extremos.
    
    Parâmetros:
        lista_valores (list): Lista de números.
    
    Retorna:
        float: Valor da mediana. Retorna 0.0 se a lista estiver vazia.
    """
    if not lista_valores:
        return 0.0

    lista_valores.sort()
    tamanho = len(lista_valores)
    meio = tamanho // 2

    # Lista com tamanho ímpar — retorna o valor central
    if tamanho % 2 != 0:
        return lista_valores[meio]

    # Lista com tamanho par — retorna a média dos dois valores centrais
    else:
        valor1 = lista_valores[meio - 1]
        valor2 = lista_valores[meio]
        return (valor1 + valor2) / 2.0


def tratamento(caminho, caminho_novo, med_peso, med_comprimento, med_altura, med_largura):
    """
    Realiza o tratamento completo do CSV de produtos.
    
    Corrige nulos na categoria (→ "Sem categoria"), aplica Regex
    e preenche dimensões físicas nulas com a mediana calculada.
    
    Parâmetros:
        caminho (str): Caminho do arquivo original.
        caminho_new (str): Caminho do arquivo de saída limpo.
        med_peso, med_comprimento, med_altura, med_largura (float): Medianas.
    
    Retorna:
        tuple: (total de linhas processadas, total de nulos corrigidos)
    """
    linhas_produtos = 0
    nulos_produtos = 0

    with open(caminho, mode='r', encoding='utf-8') as infile:
        with open(caminho_novo, mode='w', encoding='utf-8', newline='') as outfile:

            leitor = csv.DictReader(infile)
            escrita = csv.DictWriter(outfile, fieldnames=leitor.fieldnames)
            escrita.writeheader()  # escreve o cabeçalho no arquivo de saída

            for linha in leitor:
                linhas_produtos += 1

                # ===== TRATAMENTO DE CATEGORIA =====
                # Conta o nulo antes de corrigir
                if not linha['product_category_name'] or linha['product_category_name'].strip() == '':
                    nulos_produtos += 1
                # Aplica limpeza: minúsculas + strip + Regex
                linha['product_category_name'] = limpar_texto(linha['product_category_name'])

                # ===== TRATAMENTO DE DIMENSÕES FÍSICAS =====
                # Preenche com a mediana quando o valor está ausente
                if not linha['product_weight_g'] or linha['product_weight_g'].strip() == '':
                    linha['product_weight_g'] = med_peso
                    nulos_produtos += 1

                if not linha['product_length_cm'] or linha['product_length_cm'].strip() == '':
                    linha['product_length_cm'] = med_comprimento
                    nulos_produtos += 1

                if not linha['product_height_cm'] or linha['product_height_cm'].strip() == '':
                    linha['product_height_cm'] = med_altura
                    nulos_produtos += 1

                if not linha['product_width_cm'] or linha['product_width_cm'].strip() == '':
                    linha['product_width_cm'] = med_largura
                    nulos_produtos += 1

                escrita.writerow(linha)  # salva a linha tratada no arquivo de saída

    print("Arquivo atualizado com sucesso!")
    return linhas_produtos, nulos_produtos


def validacao_hipotese_pedidos(caminho_pedidos):
    """
    Valida a hipótese da Olist sobre pedidos sem data de entrega.
    
    Verifica se todos os pedidos com 'order_delivered_customer_date'
    vazia estão com status 'canceled', conforme hipótese da diretoria.
    
    Parâmetros:
        caminho_pedidos (str): Caminho do arquivo CSV de pedidos.
    """
    # Contadores para a análise
    total_nulos = 0
    nulos_cancelados = 0
    nulos_outros_status = {}  # dicionário para agrupar outros status encontrados

    with open(caminho_pedidos, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            data_entrega = linha['order_delivered_customer_date']
            status = linha['order_status']

            # Filtra apenas registros sem data de entrega
            if not data_entrega or data_entrega.strip() == '':
                total_nulos += 1

                # Classifica o status do pedido sem data
                if status == "canceled":
                    nulos_cancelados += 1
                elif status == "unavailable":
                    nulos_outros_status["unavailable"] = nulos_outros_status.get('unavailable', 0) + 1
                else:
                    nulos_outros_status[status] = nulos_outros_status.get(status, 0) + 1

    # Exibe os resultados da análise
    print(f"Total de pedidos SEM data de entrega: {total_nulos}")
    print(f"Desses, quantos estavam cancelados? {nulos_cancelados}")

    # Valida a hipótese de negócio
    if nulos_cancelados == total_nulos:
        print("\nCONCLUSÃO: Hipótese confirmada. Todos os nulos são cancelamentos.")
    else:
        print("\nCONCLUSÃO: A hipótese da Olist está ERRADA.")
        print(f"Existem {total_nulos - nulos_cancelados} pedidos sem data que não estão cancelados.")
        print("Motivos reais encontrados (Status: Quantidade):")
        for outro_status, quantidade in nulos_outros_status.items():
            print(f"  -> {outro_status}: {quantidade}")
    print("-" * 43)


def tratamento_pedidos(caminho_origem, caminho_destino):
    """
    Limpa a base de pedidos: descarta cancelados e formata datas.
    
    Remove pedidos com status 'canceled' ou 'unavailable' e
    converte a data de aprovação para o formato brasileiro.
    
    Parâmetros:
        caminho_origem (str): Caminho do CSV original de pedidos.
        caminho_destino (str): Caminho do CSV de saída limpo.
    
    Retorna:
        tuple: (total de linhas lidas, total de cancelados encontrados)
    """
    print("\nIniciando a limpeza da base de pedidos...")
    pedidos_salvos = 0
    pedidos_descartados = 0
    linhas_pedidos = 0
    cancelados = 0

    with open(caminho_origem, mode='r', encoding='utf-8') as infile:
        with open(caminho_destino, mode='w', encoding='utf-8', newline='') as outfile:
            leitura = csv.DictReader(infile)
            escrita = csv.DictWriter(outfile, fieldnames=leitura.fieldnames)
            escrita.writeheader()

            for linha in leitura:
                linhas_pedidos += 1
                status = linha['order_status']

                # Contabiliza cancelados antes de descartar
                if status == 'canceled':
                    cancelados += 1

                # Descarta pedidos cancelados e indisponíveis
                if status == 'canceled' or status == 'unavailable':
                    pedidos_descartados += 1
                    continue  # pula para a próxima linha sem salvar

                # Formata a data de aprovação para padrão brasileiro
                linha['order_approved_at'] = formatar_data(linha['order_approved_at'])

                escrita.writerow(linha)
                pedidos_salvos += 1

    print(f"Limpeza concluída! Pedidos válidos salvos: {pedidos_salvos}. Descartados: {pedidos_descartados}.")
    return linhas_pedidos, cancelados


def gerar_relatorio_final(total_linhas, nulos_corrigidos, cancelados_identificados):
    """
    Exibe o relatório estatístico final do pipeline de sanitização.
    
    Parâmetros:
        total_linhas (int): Total de linhas processadas (produtos + pedidos).
        nulos_corrigidos (int): Total de valores nulos corrigidos.
        cancelados_identificados (int): Total de pedidos cancelados encontrados.
    """
    print("\n" + "=" * 55)
    print(" RELATÓRIO FINAL DE SANITIZAÇÃO DA OLIST ".center(55, "="))
    print("=" * 55)
    print(f"  Linhas Totais Processadas:        {total_linhas}")
    print(f"  Nulos Identificados/Corrigidos:   {nulos_corrigidos}")
    print(f"  Pedidos Cancelados Identificados: {cancelados_identificados}")
    print("-" * 55)

    # Valida se o processamento foi realizado com sucesso
    if nulos_corrigidos >= 0 and total_linhas > 0:
        print("  STATUS DA BASE: 100% SANITIZADA ✓")
    else:
        print("  ATENÇÃO: Nenhuma linha foi processada.")
    print("=" * 55 + "\n")