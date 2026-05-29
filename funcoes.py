import csv
#criação do comando para realizar a leitura do arquivo csv: produtos
with open('data/olist_products_dataset.csv',mode='r',encoding='utf-8') as produto:
    leitor_csv=csv.DictReader(produto)
    for linha in leitor_csv:
        print(linha)