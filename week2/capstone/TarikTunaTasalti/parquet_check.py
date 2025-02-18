from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

def print_parquet_column_info(parquet_paths):
    """
    Her bir Parquet dosyasını okuyup kolonların veri tiplerini, NA değer sayılarını
    ve churn==1 olan satırların toplam satırlara oranını yazdırır.
    """
    spark = SparkSession.builder.appName("Parquet_Column_Info").getOrCreate()
    
    for path in parquet_paths:
        df = spark.read.parquet(f"../../../tt_data/processed/{path.split('/')[-1]}")
        
        print(f"Parquet Dosyası: {path}")
        print("Kolon Adı | Veri Tipi | NA Değer Sayısı")
        print("--------------------------------------------------")
        
        na_counts = df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).collect()[0].asDict()
        for column, na_count in na_counts.items():
            dtype = dict(df.dtypes)[column]
            print(f"{column} | {dtype} | {na_count}")
        
        # churn == 1 olanların oranını hesapla
        total_count = df.count()
        churn_count = df.filter(col("churn") == 1).count()
        churn_ratio = (churn_count / total_count) if total_count > 0 else 0
        print(f"Churn==1 Oranı: {churn_ratio:.4f}")
        print("\n")

if __name__ == "__main__":
    parquet_files = ["Broadband.parquet", "Postpaid.parquet", "Prepaid.parquet"]
    print_parquet_column_info(parquet_files)
