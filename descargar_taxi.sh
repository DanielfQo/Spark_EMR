#!/bin/bash

mkdir -p ~/taxi_data
cd ~/taxi_data

for y in 2024 2025
do
  for m in {01..12}
  do
    echo "Descargando yellow_tripdata_${y}-${m}.parquet"

    wget -q \
      https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${y}-${m}.parquet

  done
done

hdfs dfs -mkdir -p /user/hadoop/taxi

hdfs dfs -put *.parquet /user/hadoop/taxi/

hdfs dfs -ls /user/hadoop/taxi