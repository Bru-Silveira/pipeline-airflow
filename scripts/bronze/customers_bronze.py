import os
from pyspark.sql import SparkSession

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
landing_path = os.path.join(base_path, 'dados', 'landing')
bronze_path = os.path.join(base_path, 'dados', 'bronze')

def processar_customers_bronze():
    spark = SparkSession.builder.appName("processar_customers").getOrCreate()

    caminho_arquivo = os.path.join(landing_path, 'customers.json')
    destino_parquet = os.path.join(bronze_path, 'customers_bronze.parquet')

    try:
        df = spark.read.json(caminho_arquivo)
        if df.count() == 0:
            print("⚠️ Arquivo customers.json está vazio.")
        else:
            df.write.mode('overwrite').parquet(destino_parquet)
            print(f"💾 customers_bronze.parquet salvo em {destino_parquet}")
    except Exception as e:
        print(f"❌ Erro ao processar customers.json: {e}")

    spark.stop()

if __name__ == "__main__":
    processar_customers_bronze()
