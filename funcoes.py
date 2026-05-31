import csv
import re
from datetime import datetime

#FUNÇÃO REGEXE: Auxilia na padronização e aplica regra REGEX nas strings da categoria
def limpar_texto(texto):
    if not texto or texto.strip() == '': #verifica se a string é vazia ou o dado é nulo
        return "Sem categoria"
    
    texto_limpo=texto.lower() #conversão para minusculas
    texto_limpo=texto_limpo.strip() #remoção dos espaços em branco inicio e fi,
    texto_limpo=re.sub(r'[^\w\s]',"", texto_limpo) #Expressão Regular:Substitui o que não for letra, numero, espaço ou sublinha por ''

#Proteção:Se após a o REGEX a string ficou vazia
    if texto_limpo.strip() == '':
        return "Sem categoria"
    
    return texto_limpo

#Função Formatar DATA:
# Função Formatar DATA
def formatar_data(data_string):
    # Verifica se a data está vazia ou nula antes de converter
    if not data_string or data_string.strip() == '':
        return ''
    try:
        # Converte string → objeto datetime
        data_obj = datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
        # Converte objeto datetime → formato brasileiro
        data_formatada = data_obj.strftime('%d/%m/%Y')
        return data_formatada
    except ValueError:
        # Se o formato for inesperado, mantém o valor original
        return data_string


#Função que a realiza a leitura da tabela pedidos:
def leitura_csv(caminho):
    produtos=[] 
    with open(caminho,mode='r',encoding='utf-8') as produto:
        leitor_csv=csv.DictReader(produto)
        for linha in leitor_csv:
            produtos.append(linha) 

    return produtos

#Função Extrair NUMEROS 
def extrair_valores(caminho,nome_coluna):
    valores=[]

    with open(caminho,mode='r',encoding='utf-8') as arquivo:
        leitor=csv.DictReader(arquivo)

        for linha in leitor:
            dado_bruto=linha[nome_coluna]

            if dado_bruto and dado_bruto.strip() !=  '':
                numero=float(dado_bruto)

                valores.append(numero)
    return valores

#Função calcular a mediana:
def calcular_mediana(lista_valores):
    if not lista_valores:
        return 0.0
    
    lista_valores.sort()

    tamanho=len(lista_valores)

    meio=tamanho//2

    if tamanho %2 != 0:
        return lista_valores[meio]
    else:
        valor1=lista_valores[meio-1]
        valor2=lista_valores[meio]

        media_dos_centrais=(valor1+valor2)/2.0
        return media_dos_centrais   


#função para realizar o tratamento valor nulo,vazio, mediana 
def tratamento(caminho, caminho_new, med_peso, med_comprimento, med_altura, med_largura):
    linhas_produtos=0
    nulos_produtos=0
#abertura do arquivo original \ e abre um novo arquivo para escrita
    with open(caminho, mode='r', encoding='utf-8') as infile:
     
        with open(caminho_new, mode='w', encoding='utf-8', newline='') as outfile:
    
            reader = csv.DictReader(infile) #arquivo original, leitura
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames) #arquivo novo para escrever 
    
    # Escreve o cabeçalho no novo arquivo
            writer.writeheader()
    
    #Laço que percorre cada e encontra valor nulo/vazio na tabela de produto ou categoria
            for row in reader:
                linhas_produtos+=1

                if not row['product_category_name'] or row['product_category_name'].strip() == '':
                    nulos_produtos+=1
                
                row['product_category_name']=limpar_texto(row['product_category_name'])

                #----- TRATAMENTO DE DIMENSÕES-----------
                if not row['product_weight_g'] or row['product_weight_g'].strip()=='':
                    row['product_weight_g']=med_peso
                    nulos_produtos+=1
                
                if not row['product_length_cm'] or row['product_length_cm'].strip()=='':
                    row['product_length_cm']=med_comprimento
                    nulos_produtos+=1

                if not row['product_height_cm'] or row['product_height_cm'].strip()=='':
                    row['product_height_cm']=med_altura
                    nulos_produtos+=1

                if not row['product_width_cm'] or row['product_width_cm'].strip()=='':
                    row['product_width_cm']=med_largura
                    nulos_produtos+=1
             

                writer.writerow(row) #escreve a linha original/linha substuida pelo sem categoria
    print("Arquivo atualizado com sucesso!")
    return linhas_produtos,nulos_produtos


def validacao_hipotese_pedidos(caminho_pedidos):
    #contadores
    total_nulos=0
    nulos_cancelados=0
    nulos_outros_status={}

    with open(caminho_pedidos,mode='r',encoding='utf-8') as arquivo:
        leitor=csv.DictReader(arquivo)

        for linha in leitor:
            data_entrega=linha['order_delivered_customer_date']
            status=linha['order_status']

            #Registro não apresenta data de entrega?
            if not data_entrega or data_entrega.strip()== '':
                total_nulos +=1

                #2:Validação da hipotese
                if status == "canceled":
                    nulos_cancelados +=1

                elif status == "unavailable":
                    nulos_outros_status["unavailable"]=nulos_outros_status.get('unavailable',0)+1

                else:
                    nulos_outros_status[status]=nulos_outros_status.get(status,0)+1

    print(f"Total de pedidos SEM data de entrega: {total_nulos}")
    print(f"Desses, quantos estavam cancelados? {nulos_cancelados}")

    #Validacao Hipóteses de Negócios
    if nulos_cancelados == total_nulos:
        print("\nCONCLUSÃO:Hipótese da Olist apresenta fundamentos. Todos os nulos são cancelamentos")
    else:
        print("\nCONCLUSÃO: A hipótese da Olist está ERRADA")
        print(f"Existem {total_nulos - nulos_cancelados} pedidos sem data de entrega que não estão cancelados.")
        print("Motivos reais encontrados (Status: Quantidade):")
        for outro_status,quantidade in nulos_outros_status.items():
            print(f"-> {outro_status}:{quantidade}")
    print("-"*43)

   
  
def tratamento_pedidos(caminho_origem, caminho_destino):
    print("\nIniciando a limpeza da base de pedidos...")
    pedidos_salvos=0
    pedidos_descartados=0
    linhas_pedidos=0
    cancelados=0

    with open(caminho_origem, mode='r', encoding='utf-8') as infile:
        with open(caminho_destino,mode='w',encoding='utf-8', newline='') as outfile:
            leitura=csv.DictReader(infile)
            escrita=csv.DictWriter(outfile, fieldnames=leitura.fieldnames)
            escrita.writeheader()

            for linha in leitura:
                linhas_pedidos+=1
                status=linha['order_status']

                if status == 'canceled':
                     cancelados+=1

                if status=='canceled' or status =='unavailable':
                    pedidos_descartados+=1
                    continue

                linha['order_approved_at']=formatar_data(linha['order_approved_at'])

                escrita.writerow(linha)
                pedidos_salvos+=1
    print(f"Limpeza concluída!Pedidos válidos slavos: {pedidos_salvos}.Descartados:{pedidos_descartados}.")
    return linhas_pedidos,cancelados

def gerar_relatorio_final(total_linhas,nulos_corrigidos,cancelados_identificados):
    print("\n" + "="*55)
    print(" RELATÓRIO FINAL DE SANITIZAÇÃO DA OLIST ".center(55,"="))
    print("="*55)
    print(f"Linhas Totais Processadas: {total_linhas}")
    print(f" Nulos Identificados/Salvos: {nulos_corrigidos}")
    print(f"Pedidos Cancelados: {cancelados_identificados}")
    print("_"*55)

    if total_linhas>0:
        print("STATUS DA BASE: 100% SANITIZADA")
    else:
        print("Nenhuma linha foi porecossada")
    print("="*55 +"\n")