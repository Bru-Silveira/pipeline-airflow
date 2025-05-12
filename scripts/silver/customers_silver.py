import os
from pyspark.sql import SparkSession

def iniciar_sessao_spark():
    return SparkSession.builder.appName("Remover Prefixo das Colunas").getOrCreate()

def remover_prefixo(df, prefixo):
    novas_colunas = [col.replace(prefixo, '') for col in df.columns]
    return df.toDF(*novas_colunas)

def processar_customers_silver():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    bronze_path = os.path.join(base_path, 'dados', 'bronze', 'customers_bronze.parquet')
    silver_path = os.path.join(base_path, 'dados', 'silver', 'customers_silver.parquet')
    prefixo = "customer_"

    spark = iniciar_sessao_spark()
    df = spark.read.parquet(bronze_path)
    df_sem_prefixo = remover_prefixo(df, prefixo)

    print("📄 Schema após remoção do prefixo (customers):")
    df_sem_prefixo.printSchema()

    df_sem_prefixo.write.mode('overwrite').parquet(silver_path)
    print(f"💾 Arquivo salvo em: {silver_path}")

    spark.stop()

if __name__ == "__main__":
    processar_customers_silver()
