#!/bin/bash

hdfs dfs -mkdir -p /user/hadoop/data

hadoop fs -cp \
s3://hdfs-hadoop-dquinones/data/* \
hdfs:///user/hadoop/data/
