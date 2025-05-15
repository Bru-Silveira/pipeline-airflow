import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum

# Função para iniciar a sessão Spark
def iniciar_sessao_spark():
    return SparkSession.builder \
        .appName("Processar Camada Gold") \
        .getOrCreate()

# Função para obter caminho base do projeto
def get_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Função principal para processar dados da camada Gold
def processar_dados_gold():
    base_path = get_base_path()

    # Caminhos dinâmicos
    caminho_silver_orders = os.path.join(base_path, 'dados', 'silver', 'orders_silver.parquet')
    caminho_silver_order_items = os.path.join(base_path, 'dados', 'silver', 'order_items_silver.parquet')
    caminho_silver_customers = os.path.join(base_path, 'dados', 'silver', 'customers_silver.parquet')
    caminho_gold = os.path.join(base_path, 'dados', 'gold', 'pedidos_por_cidade_estado')

    # Inicia a sessão Spark
    spark = iniciar_sessao_spark()

    # Carrega os dados das tabelas Silver
    df_orders = spark.read.parquet(caminho_silver_orders)
    df_order_items = spark.read.parquet(caminho_silver_order_items)
    df_customers = spark.read.parquet(caminho_silver_customers)

    # Agrega dados dos itens por pedido
    df_order_items_aggregated = df_order_items.groupBy("order_id") \
        .agg(
            sum("subtotal").alias("valor_total_pedido"),
            count("id").alias("quantidade_itens_pedido")
        )

    # Junta pedidos com itens
    df_orders_aggregated = df_orders.join(
        df_order_items_aggregated,
        df_orders.id == df_order_items_aggregated.order_id,
        how="inner"
    )

    # Junta com dados de clientes
    df_final = df_orders_aggregated.join(
        df_customers,
        df_orders_aggregated.customer_id == df_customers.id,
        how="inner"
    )

    # Agrega dados por cidade e estado
    df_gold = df_final.groupBy("city", "state") \
        .agg(
            count("order_id").alias("quantidade_pedidos"),
            sum("valor_total_pedido").alias("valor_total_pedidos")
        )

    # Exibe resultado
    print("Esquema do DataFrame Gold:")
    df_gold.printSchema()

    print("Prévia dos dados gerados para a camada Gold:")
    df_gold.show(truncate=False)

    # Salva os dados
    df_gold.write.mode("overwrite").parquet(caminho_gold)

    # Encerra a sessão
    spark.stop()

# Executa a função principal
if __name__ == "__main__":
    processar_dados_gold()
