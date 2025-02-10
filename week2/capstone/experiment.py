from typing import Dict, List

import click
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, size

ALL_COLUMNS = [
    "service_type",
    "app",
    "avg_call_duration",
    "avg_top_up_count",
    "call_drops",
    "id",
    "roaming_usage",
    "apps",
    "churn",
    "auto_payment",
    "tenure",
    "age",
    "apps_count",
    "customer_support_calls",
    "data_usage",
    "monthly_charge",
    "overdue_payments",
    "satisfaction_score",
]

RELEVANT_COLUMNS_DICT: Dict[str, List[str]] = {
    "Broadband": [
        "auto_payment",
        "tenure",
        "age",
        "apps_count",
        "customer_support_calls",
        "data_usage",
        "monthly_charge",
        "overdue_payments",
        "satisfaction_score",
    ],
    "Prepaid": [
        "avg_call_duration",
        "avg_top_up_count",
        "call_drops",
        "roaming_usage",
        "tenure",
        "age",
        "apps_count",
        "customer_support_calls",
        "data_usage",
        "monthly_charge",
        "satisfaction_score",
    ],
    "Postpaid": [
        "avg_call_duration",
        "call_drops",
        "roaming_usage",
        "auto_payment",
        "tenure",
        "age",
        "apps_count",
        "customer_support_calls",
        "data_usage",
        "monthly_charge",
        "overdue_payments",
        "satisfaction_score",
    ],
}


def build_spark_app(name: str = "Churn Prediction Application"):
    spark = (
        SparkSession.builder.appName(name)
        .master("local[*]")
        .config("spark.driver.memory", "2g")
        .config("spark.executor.memory", "4g")
        .getOrCreate()
    )

    return spark


@click.command()
@click.option("--service-type", default="Broadband")
@click.option(
    "--file-glob",
    default="capstone.*.jsonl.gz",
    help="Pattern of files to be used for training and evaluation",
)
def cli(service_type: str, file_glob: str):
    spark = build_spark_app()

    df = spark.read.json(file_glob).withColumn("label", col("churn").cast("int"))

    relevant_columns = RELEVANT_COLUMNS_DICT.get(service_type)

    service_df = (
        df.filter(df.service_type == service_type)
        .withColumn("apps_count", size(df["apps"]))
        .drop(*list(set(ALL_COLUMNS) - set(relevant_columns)))
    )

    print(f"Number of rows for {service_type}: {service_df.count()}")

    service_df = service_df.dropna().cache()

    print(
        f"Number of rows (after removing NA rows) for {service_type}: {service_df.count()}"
    )

    v = VectorAssembler(
        inputCols=relevant_columns,
        outputCol="features",
    )

    service_df = v.transform(service_df)

    train, test = service_df.randomSplit(weights=[0.8, 0.2], seed=42)

    train.show(3)

    test.show(3)

    rf = RandomForestClassifier(maxDepth=10, numTrees=40).fit(train)

    result = rf.evaluate(test)

    print(f"AUC: {result.areaUnderROC} and Accuracy: {result.accuracy}")


if __name__ == "__main__":
    cli()
