import csv

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
    
#abertura do arquivo original \ e abre um novo arquivo para escrita
    with open(caminho, mode='r', encoding='utf-8') as infile:
     
        with open(caminho_new, mode='w', encoding='utf-8', newline='') as outfile:
    
            reader = csv.DictReader(infile) #arquivo original, leitura
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames) #arquivo novo para escrever 
    
    # Escreve o cabeçalho no novo arquivo
            writer.writeheader()
    
    #Laço que percorre cada e encontra valor nulo/vazio na tabela de produto ou categoria
            for row in reader:
        # Verifica se o valor é nulo ou vazio
        #se não tiver nada escrito (vazio) ou estiver nula 
                if not row['product_category_name'] or row['product_category_name'].strip() == '':
                    row['product_category_name'] = 'Sem Categoria'

                if not row['product_weight_g'] or row['product_weight_g'].strip()=='':
                    row['product_weight_g']=med_peso
                
                if not row['product_length_cm'] or row['product_length_cm'].strip()=='':
                    row['product_length_cm']=med_comprimento

                if not row['product_height_cm'] or row['product_height_cm'].strip()=='':
                    row['product_height_cm']=med_altura

                if not row['product_width_cm'] or row['product_width_cm'].strip()=='':
                    row['product_width_cm']=med_largura
             


                writer.writerow(row) #escreve a linha original/linha substuida pelo sem categori
    print("Arquivo atualizado com sucesso!")

  


