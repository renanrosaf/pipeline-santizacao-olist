# Pipeline de Sanitização de Dados - Olist

Pipeline de sanitização de dados em formato CSV do banco de dados da Olist. Este repositório é referente ao Mini Projeto Avaliativo 1 do curso profissionalizante em Machine Learning (SCTEC - SENAI/SC).

## Descrição do Projeto:

A equipe de Engenharia de Dados da Olist identificou inconsistências nos arquivos `olist_orders_dataset.csv` e `olist_orders_products.csv` que estavam causando falhas na geração de relatórios automatizados. 

Para solucionar esse problema, este projeto desenvolve um pipeline de sanitização de dados construído em **Python puro**. A premissa é não utilizar bibliotecas externas de análise (como o Pandas), aplicando exclusivamente as ferramentas nativas da linguagem (`csv`, `re`, `datetime`).

As principais etapas do processamento incluem:
* **Tratamento de nulos:** Correção de valores ausentes nas colunas de categoria e dimensões físicas.
* **Padronização:** Limpeza de strings e uso de Expressões Regulares (Regex) nos nomes das categorias.
* **Validação de negócio:** Verificação de regras específicas, como a de pedidos cancelados sem data de entrega.
* **Conversão de formatos:** Ajuste das datas do formato padrão ISO para o formato brasileiro (DD/MM/AAAA).
* **Relatório:** Geração de um resumo estatístico ao final da execução do pipeline.

## Dados Utilizados:

Os arquivos CSV utilizados neste projeto são públicos e podem ser baixados diretamente do Kaggle:

* [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Para executar o projeto, faça o **download** especificamente dos seguintes arquivos:
* `olist_orders_dataset.csv`
* `olist_orders_products.csv`

Após o download, mova os arquivos para a pasta `data/` no diretório do seu projeto, deixando a estrutura assim:

```text
seu-projeto/
├── data/
│   ├── olist_orders_dataset.csv
│   └── olist_orders_products.csv

```
## Estrutura do Projeto:

```text
pipeline-sanitizacao-olist/
│
├── data/
│   ├── olist_orders_products.csv
│   └── olist_orders_dataset.csv
│
├── main.py        # Script principal — orquestra o pipeline
├── funcoes.py     # Funções auxiliares de limpeza e validação
└── README.md      # Documentação do projeto
```

## Como Executar o Projeto:

### Pré Requisitos:

-Python 3.8+ instalado em sua máquina.

-Não é necessária a instalação de bibliotecas externas. O projeto utiliza apenas módulos nativos da linguagem (csv, re, datetime).

### Passo a Passo:

**1. Clone o repositório: ** 
``` bash 
git clone https://github.com/renanrosaf/pipeline-santizacao-olist.git
cd pipeline-sanitizacao-olist
```
**2. Adicione os arquivos de dados:**
Certifique-se de ter feito o download dos arquivos no Kaggle (como explicado na seção *Dados Utilizados*) e mova-os para dentro da pasta `data/` na raiz do projeto:

```text
pipeline-sanitizacao-olist/
├── data/
│   ├── olist_orders_dataset.csv
│   └── olist_orders_products.csv

```
**3. Execute o script principal:**
```bash 
python main.py
```
**4. Resultado Esperado:**
```text
Após a execução, o script exibirá no terminal um relatório estatístico estruturado da seguinte forma:

Extraindo e calculando a mediana ....
Realizando o tratamento de dados nulos e vazios...
Arquivo atualizado com sucesso!
Carregando os dados na memória...
32951 produtos e 99441 pedidos carregados

Total de pedidos SEM data de entrega: 2965
Desses, quantos estavam cancelados? 619

CONCLUSÃO: A hipótese da Olist está ERRADA
Existem 2346 pedidos sem data de entrega que não estão cancelados.
Motivos reais encontrados (Status: Quantidade):
-> invoiced:314
-> shipped:1107
-> processing:301
-> unavailable:609
-> delivered:8
-> created:5
-> approved:2

Iniciando a limpeza da base de pedidos...
Limpeza concluída! Pedidos válidos salvos: 98207. Descartados: 1234.

=======================================================
======= RELATÓRIO FINAL DE SANITIZAÇÃO DA OLIST =======
=======================================================
Linhas Totais Processadas:        132392
Nulos Identificados/Corrigidos:   618
Pedidos Cancelados Identificados: 625
=======================================================
STATUS DA BASE: 100% SANITIZADA ✓
=======================================================
```

##  Tecnologias utilizadas

* **Python 3.8**
* **Módulo `csv`:** Leitura e processamento dos arquivos estruturados.
* **Módulo `re`:** Uso de expressões regulares para a limpeza de strings.
* **Módulo `datetime`:** Manipulação, validação e formatação de datas.

## Reflexão Teórica sobre Machine Learning: Como uma lógica de programação aplicada à limpeza correta dos dados ajuda a evitar o Overfitting ou viés em futuros modelos de Inteligência Artificial.

```text
A qualidade dos dados é o pilar fundamental no treinamento de qualquer modelo de Inteligência Artificial. Se os dados não forem devidamente sanitizados, o algoritmo pode aprender padrões incorretos e amplificar vieses, resultando em previsões que não condizem com a realidade. Em contrapartida, uma limpeza bem executada é o que garante a estabilidade e a precisão das futuras análises. Quando negligenciamos essa etapa, deixamos o projeto exposto a dois riscos severos: o Viés (Bias), que ensina uma visão distorcida à máquina, e o Overfitting (Sobreajuste), onde o modelo decora ruídos e falhas em vez de generalizar os padrões reais do negócio.
É exatamente aí que entra o diferencial de aplicar a lógica de programação. Ao estruturar a limpeza de dados através de códigos e funções modulares, nós garantimos a reprodutibilidade e a escalabilidade do processo. Isso assegura que qualquer novo lote de informações passará pelo mesmo rigor estatístico, blindando o modelo e garantindo que ele evolua sobre uma base técnica sólida.
```

## Autor

**Renan Rosa Ferreira**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/renan-rosa-ferreira-1544701a3/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/renanrosaf)
