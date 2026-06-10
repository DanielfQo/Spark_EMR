from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower
import time

inicio = time.time()

spark = SparkSession.builder.appName("WordCount").getOrCreate()

df = spark.read.text("hdfs:///user/hadoop/data/*.txt")

words = df.select(
    explode(
        split(lower(df.value), "\\s+")
    ).alias("word")
)

resultado = (
    words.groupBy("word")
         .count()
         .orderBy("count", ascending=False)
)


fin = time.time()

print(f"Tiempo: {fin - inicio:.2f} segundos")

resultado.show(50, False)