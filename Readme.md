# 🛠️ Projeto de Pipeline Lakehouse com Apache Airflow e PySpark

Este repositório contém um pipeline de dados desenvolvido com Apache Airflow e PySpark, estruturado com base nas camadas **Bronze**, **Silver** e **Gold** de um modelo Lakehouse.

## 📁 Estrutura do Projeto

<pre>
.
├── dags
│   ├── dados                      # Camadas de dados no formato Data Lakehouse
│   │   ├── landing                # Dados brutos recebidos (JSON)
│   │   │   ├── customers.json
│   │   │   ├── order_item.json
│   │   │   └── orders.json
│   │   ├── bronze                 # Dados brutos convertidos para Parquet
│   │   │   ├── customers_bronze.parquet/
│   │   │   ├── order_items_bronze.parquet/
│   │   │   └── orders_bronze.parquet/
│   │   ├── silver                 # Dados limpos e estruturados
│   │   │   ├── customers_silver.parquet/
│   │   │   ├── order_items_silver.parquet/
│   │   │   └── orders_silver.parquet/
│   │   └── gold                   # Dados prontos para análise e dashboards
│   │       └── pedidos_por_cidade_estado.parquet/
│   ├── scripts                    # Scripts de transformação por camada
│   │   ├── __init__.py
│   │   ├── bronze
│   │   │   ├── customers_bronze.py
│   │   │   ├── order_items_bronze.py
│   │   │   └── orders_bronze.py
│   │   ├── silver
│   │   │   ├── customers_silver.py
│   │   │   ├── order_items_silver.py
│   │   │   └── orders_silver.py
│   │   └── gold
│   │       └── processar_gold.py
│   └── pipeline_lakehouse.py     # Pipeline principal do Airflow
└── requirements.txt
</pre>

## 🗂️ Estrutura do Pipeline

<pre>
pipeline_lakehouse
├── bronze_customers
│     └── silver_customers
│           └──
├── bronze_orders
│     └── silver_orders
│           └──
├── bronze_order_items
│     └── silver_order_items
│           └──
└──────────── gold
</pre>

## 🔄 Pipeline de Orquestração (`pipeline_lakehouse.py`)

A DAG principal `pipeline_lakehouse` executa as três etapas principais do fluxo:

1. **Camada Landing → Bronze (`bronze_customers`, `bronze_orders`, `bronze_order_items`)**:  
   - Lê arquivos JSON da camada *Landing*.
   - Converte para formato Parquet.
   - Salva os dados tratados na camada *Bronze*.

2. **Camada Bronze → Silver (`silver_customers`, `silver_orders`, `silver_order_items`)**:  
   - Lê os dados em Parquet da camada Bronze.
   - Remove prefixos das colunas e realiza transformações.
   - Salva os dados tratados na camada *Silver*.

3. **Camada Silver → Gold (`gold`)**:  
   - Realiza junções e agregações nos dados da Silver.
   - Salva os resultados analíticos na camada *Gold*.

> As tarefas de Bronze e Silver são executadas **em paralelo**, e a camada Gold só é processada após ambas serem concluídas.


## ▶️ Execução

### Pré-requisitos

- Apache Airflow instalado e configurado.
- PySpark disponível no ambiente.
- Estrutura de diretórios esperada:
O projeto assume a seguinte estrutura de pastas dentro do diretório base (resolvido dinamicamente no código):

<pre>
dados/
├── landing/
├── bronze/
├── silver/
└── gold/
</pre>

⚙️ O caminho base é detectado dinamicamente no código com:
```
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
```

### Ativando o Airflow

1. Inicialize o Airflow (apenas na primeira vez):
```bash
airflow db init
```
2. (Importante) Configure o Airflow para reconhecer as DAGs deste projeto:
* Abra o arquivo de configuração do Airflow:
* No terminal:
```bash
nano ~/airflow/airflow.cfg
```
* Ou no vs code:
```bash
code ~/airflow/airflow.cfg
```
* Localize a linha dags_folder e substitua pelo caminho completo até a pasta dags do seu projeto:
```bash
dags_folder = /home/bru_silveira/projeto-airflow/dags
```
* Salve e feche o arquivo.
3. Inicie os serviços:
```bash
airflow scheduler
airflow webserver --port 8080
```
4. Acesse a interface: http://localhost:8080

### Visualizando o Pipeline

Na UI do Airflow, você verá a DAG:

- pipeline_lakehouse ✅ (orquestradora principal)

Você pode ativar e rodar a pipeline_lakehouse para executar o pipeline completo.

### 👩‍💻 Autoria
Desenvolvido por Bruna Silveira
