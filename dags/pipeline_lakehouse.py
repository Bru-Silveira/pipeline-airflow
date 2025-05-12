import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importando as funções específicas de cada etapa
from scripts.bronze.customers_bronze import processar_customers_bronze
from scripts.bronze.orders_bronze import processar_orders_bronze
from scripts.bronze.order_items_bronze import processar_order_items_bronze

from scripts.silver.customers_silver import processar_customers_silver
from scripts.silver.orders_silver import processar_orders_silver
from scripts.silver.order_items_silver import processar_order_items_silver

from scripts.gold.processar_gold import processar_dados_gold

# Caminho base dinâmico (do diretório onde este DAG está localizado)
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Funções do pipeline
def run_bronze_to_parquet():
    print("🔶 Iniciando etapa Bronze...")
    processar_customers_bronze()
    print("✅ Customers Bronze processado.")
    processar_orders_bronze()
    print("✅ Orders Bronze processado.")
    processar_order_items_bronze()
    print("✅ Order Items Bronze processado.")
    print("✅ Etapa Bronze finalizada.\n")

def run_silver_transform():
    print("🔘 Iniciando etapa Silver...")
    processar_customers_silver()
    print("✅ Customers Silver processado.")
    processar_orders_silver()
    print("✅ Orders Silver processado.")
    processar_order_items_silver()
    print("✅ Order Items Silver processado.")
    print("✅ Etapa Silver finalizada.\n")

def run_gold():
    print("🏅 Iniciando etapa Gold...")
    processar_dados_gold()
    print("✅ Etapa Gold finalizada.\n")

# Configuração do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pipeline_lakehouse',
    default_args=default_args,
    description='Orquestra o pipeline de dados (Bronze → Silver → Gold)',
    schedule=None,
    catchup=False,
    tags=['orquestrador'],
) as dag:

     # Bronze Tasks
    bronze_customers = PythonOperator(
        task_id='bronze_customers',
        python_callable=processar_customers_bronze,
    )

    bronze_orders = PythonOperator(
        task_id='bronze_orders',
        python_callable=processar_orders_bronze,
    )

    bronze_order_items = PythonOperator(
        task_id='bronze_order_items',
        python_callable=processar_order_items_bronze,
    )

    # Silver Tasks
    silver_customers = PythonOperator(
        task_id='silver_customers',
        python_callable=processar_customers_silver,
    )

    silver_orders = PythonOperator(
        task_id='silver_orders',
        python_callable=processar_orders_silver,
    )

    silver_order_items = PythonOperator(
        task_id='silver_order_items',
        python_callable=processar_order_items_silver,
    )

    # Gold Task
    gold = PythonOperator(
        task_id='gold',
        python_callable=processar_dados_gold,
    )

    # Dependências: Paralelizando Bronze e Silver, e Gold depois do Silver
    # Bronze Tasks (paralelizadas)
    bronze_tasks = [bronze_customers, bronze_orders, bronze_order_items]
    
    # Silver Tasks (paralelizadas, após a conclusão das tarefas Bronze)
    silver_tasks = [silver_customers, silver_orders, silver_order_items]

    # Encadeando as dependências
    for task in bronze_tasks:
        task >> silver_tasks

    for task in silver_tasks:
        task >> gold
