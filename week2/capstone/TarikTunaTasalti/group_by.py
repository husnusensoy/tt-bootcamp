from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def group_by_service_type(file_paths):
    """
    JSON dosyalarını okuyup service_type değişkenine göre gruplar.
    """
    spark = SparkSession.builder.appName("JSON_to_CSV_with_Lists").getOrCreate()
    
    # Tüm dosyaları oku ve birleştir
    df = spark.read.json(file_paths)
    
    # service_type'a göre gruplandır
    service_types = df.select("service_type").distinct().rdd.flatMap(lambda x: x).collect()
    grouped_data = {service_type: df.filter(col("service_type") == service_type) for service_type in service_types}
    
    return grouped_data

def save_to_parquet(grouped_data, output_path):
    """
    Verileri belirlenen yola parquet formatında kaydeder.
    """
    for service_type, df in grouped_data.items():
        df.write.parquet(f"{output_path}/{service_type}.parquet", mode="overwrite")

if __name__ == "__main__":
    file_paths = [f"../../../tt_data/capstone.{i}.jsonl" for i in range(1, 11)]
    parquet_output_path = "../../../tt_data/"
    grouped_data = group_by_service_type(file_paths)
    save_to_parquet(grouped_data, parquet_output_path)
