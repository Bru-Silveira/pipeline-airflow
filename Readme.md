# 🛠️ Projeto de Pipeline Lakehouse com Apache Airflow e PySpark

Este repositório contém um pipeline de dados desenvolvido com Apache Airflow e PySpark, estruturado com base nas camadas **Bronze**, **Silver** e **Gold** de um modelo Lakehouse.

## 📁 Estrutura do Projeto

dags/
├── json_to_bronze.py # DAG responsável por transformar arquivos JSON em Parquet (camada Bronze)
├── data_to_silver.py # DAG que remove prefixos das colunas e gera a camada Silver
├── processar_gold.py # DAG que gera os dados agregados para a camada Gold
├── pipeline_lakehouse.py # DAG principal que orquestra todas as etapas do pipeline

## 🗂️ Estrutura do Pipeline

├── landing/                  # Dados brutos recebidos em formato JSON
│ └── arquivos_json/          # Subpastas com arquivos JSON por entidade
│     ├── customers/
│     ├── orders/
│     └── order_item/
│
├── bronze/                  # Dados convertidos de JSON para Parquet
│   ├── customers/
│   ├── orders/
│   └── order_item/
│
├── silver/                  # Dados tratados e limpos
│   ├── customers/
│   ├── orders/
│   └── order_item/
│
└── gold/                    # Dados prontos para consumo analítico
    └── pedidos_por_cidade_estado/


## 🔄 Pipeline de Orquestração (`pipeline_lakehouse.py`)

A DAG principal `pipeline_lakehouse` executa as três etapas principais do fluxo:

1. **Camada Landing → Bronze (`json_to_bronze_task`)**:  
   - Lê arquivos JSON da camada *Landing*.
   - Converte para formato Parquet.
   - Salva os dados tratados na camada *Bronze*.

2. **Camada Bronze → Silver (`data_to_silver_task`)**:  
   - Lê os dados em Parquet da camada Bronze.
   - Remove prefixos das colunas e realiza transformações.
   - Salva os dados tratados na camada *Silver*.

3. **Camada Silver → Gold (`processar_gold_task`)**:  
   - Realiza junções e agregações nos dados da Silver.
   - Salva os resultados analíticos na camada *Gold*.

> As tarefas de Bronze e Silver são executadas **em paralelo**, e a camada Gold só é processada após ambas serem concluídas.

## ▶️ Execução

### Pré-requisitos

- Apache Airflow instalado e configurado.
- PySpark disponível no ambiente.
- Estrutura de diretórios criada:

/home/bru_silveira/airflow/lakehouse/
├── landing/
├── bronze/
├── silver/
└── gold/

### Ativando o Airflow

```bash
# Inicialize o Airflow
airflow db init
airflow scheduler
airflow webserver --port 8080
```

Acesse a interface: http://localhost:8080

### Visualizando o Pipeline

Na UI do Airflow, você verá as DAGs:

- json_to_bronze

- data_to_silver

- processar_gold

- pipeline_lakehouse ✅ (orquestradora principal)

Você pode ativar e rodar qualquer uma separadamente, ou a pipeline_lakehouse para executar o pipeline completo.

### 👩‍💻 Autoria
Desenvolvido por Bruna Silveira
