from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, size, mode, median

def read_parquet_and_count_nulls(parquet_paths):
    """
    Her bir Parquet dosyasını okuyup toplam satır sayısını ve her kolondaki NA değer sayısını hesaplar.
    """
    spark = SparkSession.builder.appName("Parquet_Statistics").getOrCreate()
    
    parquet_data = {}
    
    for path in parquet_paths:
        df = spark.read.parquet(path)
        total_rows = df.count()
        
        # NA değerlerini hesapla her kolon için
        na_counts = df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns])
        na_counts_dict = na_counts.collect()[0].asDict()
        
        print(f"Parquet Dosyası: {path}")
        print(f"Toplam Satır Sayısı: {total_rows}")
        print("Her Kolondaki NA Değer Sayısı:")
        for column, na_count in na_counts_dict.items():
            print(f"  {column}: {na_count}")
        print("\n")
        
        parquet_data[path] = df
    
    return parquet_data

def drop_unwanted_columns(parquet_data):
    """
    Broadband.parquet dosyasından avg_call_duration, call_drops ve roaming_usage kolonlarını,
    Prepaid.parquet dosyasından auto_payment kolonunu drop eder.
    """
    for path, df in parquet_data.items():
        if "Broadband.parquet" in path:
            parquet_data[path] = df.drop("avg_call_duration", "call_drops", "roaming_usage")
        elif "Prepaid.parquet" in path:
            parquet_data[path] = df.drop("auto_payment","overdue_payments")
        elif "Postpaid.parquet" in path:
            parquet_data[path] = df.drop("avg_top_up_count")
            
    return parquet_data

def fill_na_values(parquet_data):
    """
    Eksik değerleri doldurma işlemi:
    - Broadband.parquet: auto_payment'ı mod ile, monthly_charge'ı medyan ile, tenure NA olanları drop eder.
    - Postpaid.parquet: auto_payment'ı mod ile, data_usage ve monthly_charge'ı medyan ile, tenure NA olanları drop eder.
    - Prepaid.parquet: avg_call_duration, data_usage ve monthly_charge'ı medyan ile, tenure NA olanları drop eder.
    """
    for path, df in parquet_data.items():
        if "Broadband.parquet" in path:
            mode_payment = df.select(mode("auto_payment")).collect()[0][0]
            median_charge = df.select(median("monthly_charge")).collect()[0][0]
            median_data = df.select(median("data_usage")).collect()[0][0]
            df = df.fillna({"auto_payment": mode_payment, "monthly_charge": median_charge,
                            "data_usage": median_data})
            df = df.na.drop(subset=["tenure"])
        elif "Postpaid.parquet" in path:
            mode_payment = df.select(mode("auto_payment")).collect()[0][0]
            median_call = df.select(median("avg_call_duration")).collect()[0][0]
            median_data = df.select(median("data_usage")).collect()[0][0]
            median_charge = df.select(median("monthly_charge")).collect()[0][0]
            df = df.fillna({"auto_payment": mode_payment,"avg_call_duration": median_call,
                            "data_usage": median_data, "monthly_charge": median_charge})
            df = df.na.drop(subset=["tenure"])
        elif "Prepaid.parquet" in path:
            median_call = df.select(median("avg_call_duration")).collect()[0][0]
            median_data = df.select(median("data_usage")).collect()[0][0]
            median_charge = df.select(median("monthly_charge")).collect()[0][0]
            df = df.fillna({"avg_call_duration": median_call, "data_usage": median_data, 
                            "monthly_charge": median_charge})
            df = df.na.drop(subset=["tenure"])
        
        parquet_data[path] = df
    
    return parquet_data

def preprocess_columns(parquet_data):
    """
    - 'apps' kolonunu listedeki eleman sayısı ile değiştirir ve 'apps' kolonunu siler.
    - 'service_type' kolonunu drop eder.
    - bigint türündeki kolonları integer'a, boolean türündeki kolonları integer'a çevirir.
    """
    for path, df in parquet_data.items():
        for column, dtype in df.dtypes:
            if dtype == "bigint":
                df = df.withColumn(column, col(column).cast("int"))
            elif dtype == "boolean":
                df = df.withColumn(column, col(column).cast("int"))
        
        if "apps" in df.columns:
            df = df.withColumn("apps_count", size(col("apps"))).drop("apps")
        if "service_type" in df.columns:
            df = df.drop("service_type")
        parquet_data[path] = df
    
    return parquet_data

def write_parquet(parquet_data, output_dir="../../../tt_data/processed"):
    """
    Temizlenmiş ve düzenlenmiş Parquet verilerini diske kaydeder.
    """
    for path, df in parquet_data.items():
        filename = path.split("/")[-1]
        df.write.parquet(f"{output_dir}/{filename}", mode="overwrite")
        print(f"Processed Parquet saved: {output_dir}/{filename}")

if __name__ == "__main__":
    parquet_files = ["../../../tt_data/Broadband.parquet", "../../../tt_data/Postpaid.parquet", "../../../tt_data/Prepaid.parquet"]
    parquet_data = read_parquet_and_count_nulls(parquet_files)
    parquet_data = drop_unwanted_columns(parquet_data)
    parquet_data = fill_na_values(parquet_data)
    parquet_data = preprocess_columns(parquet_data)
    write_parquet(parquet_data)
