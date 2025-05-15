import os
from pyspark.sql import SparkSession

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
landing_path = os.path.join(base_path, 'dados', 'landing')
bronze_path = os.path.join(base_path, 'dados', 'bronze')

def processar_order_items_bronze():
    spark = SparkSession.builder.appName("processar_order_items").getOrCreate()

    caminho_arquivo = os.path.join(landing_path, 'order_item.json')
    destino_parquet = os.path.join(bronze_path, 'order_items_bronze.parquet')

    try:
        df = spark.read.json(caminho_arquivo)
         # Visualizar colunas antes de qualquer processamento
        print("📄 Esquema do arquivo order_item.json:")
        df.printSchema()
        print("🔍 Colunas encontradas:", df.columns)
        if df.count() == 0:
            print("⚠️ Arquivo order_item.json está vazio.")
        else:
            df.write.mode('overwrite').parquet(destino_parquet)
            print(f"💾 order_items_bronze.parquet salvo em {destino_parquet}")
    except Exception as e:
        print(f"❌ Erro ao processar order_item.json: {e}")

    spark.stop()

if __name__ == "__main__":
    processar_order_items_bronze()