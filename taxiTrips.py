from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month
import time


# Crear Spark Session
spark = (SparkSession.builder.appName("NYC Taxi Trips Analysis").getOrCreate())

# Cargar Dataset

print("Cargando datos")

df = spark.read.parquet(
    "s3a://hdfs-hadoop-dquinones/data/*.parquet"
)

print(f"Total registros: {df.count()}")

# Particionamiento

print("Particiones")

df_partitioned = (
    df.withColumn(
        "year",
        year("tpep_pickup_datetime")
    )
    .withColumn(
        "month",
        month("tpep_pickup_datetime")
    )
)

df_partitioned.write \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet(
        "s3a://hdfs-hadoop-dquinones/taxi_partitioned"
    )

# Crear Vista SQL

df.createOrReplaceTempView("taxi_trips")

# Consulta 1

print("\nTOTAL DE VIAJES")

inicio = time.time()

spark.sql("""
SELECT COUNT(*) AS total_viajes
FROM taxi_trips
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

# Consulta 2

print("\nDISTANCIA PROMEDIO")

inicio = time.time()

spark.sql("""
SELECT AVG(trip_distance)
AS distancia_promedio
FROM taxi_trips
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

# Consulta 3

print("\nHORAS DE MAYOR TRAFICO")

inicio = time.time()

spark.sql("""
SELECT
    HOUR(tpep_pickup_datetime) AS hora,
    COUNT(*) AS total_viajes
FROM taxi_trips
GROUP BY HOUR(tpep_pickup_datetime)
ORDER BY total_viajes DESC
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

# Consulta 4

print("\nMETODOS DE PAGO")

inicio = time.time()

spark.sql("""
SELECT
    payment_type,
    COUNT(*) AS cantidad
FROM taxi_trips
GROUP BY payment_type
ORDER BY cantidad DESC
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

# Consulta 5

print("\nTOP 10 VIAJES MAS COSTOSOS")

inicio = time.time()

spark.sql("""
SELECT
    fare_amount,
    trip_distance,
    tpep_pickup_datetime
FROM taxi_trips
ORDER BY fare_amount DESC
LIMIT 10
""").show(truncate=False)

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

# Consulta 6

print("\nCONSULTA PARTICIONADA")

df_part = spark.read.parquet(
    "s3a://hdfs-hadoop-dquinones/taxi_partitioned"
)

df_part.createOrReplaceTempView("taxi_part")

#Sin particionar

print("\nSIN PARTICIONAR")

inicio = time.time()

spark.sql("""
SELECT COUNT(*) AS viajes_enero_2024
FROM taxi_trips
WHERE YEAR(tpep_pickup_datetime)=2024
AND MONTH(tpep_pickup_datetime)=1
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")

#Con particionar

print("\nCON PARTICIONAR")

inicio = time.time()

spark.sql("""
SELECT COUNT(*) AS viajes_enero_2024
FROM taxi_part
WHERE year=2024
AND month=1
""").show()

print(f"Tiempo: {time.time()-inicio:.2f} segundos")


spark.stop()