from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode,
    split,
    lower,
    input_file_name,
    collect_set,
    regexp_replace
)

import time

inicio = time.time()

spark = SparkSession.builder \
    .appName("IndiceInvertido") \
    .getOrCreate()

df = spark.read.text(
    "s3a://hdfs-hadoop-dquinones/data/*.txt"
)

df = df.withColumn(
    "documento",
    input_file_name()
)

tokens = df.select(
    explode(
        split(
            lower(regexp_replace("value", r"[^a-zA-Záéíóúñü0-9 ]", "")),r"\s+"
        )
    ).alias("palabra"),
    "documento"
)

tokens = tokens.filter(tokens.palabra != "")

indice = (
    tokens.groupBy("palabra")
          .agg(
              collect_set("documento")
              .alias("documentos")
          )
          .orderBy("palabra")
)

fin = time.time()

print(f"Tiempo: {fin - inicio:.2f} segundos")


indice.show(50, truncate=False)

