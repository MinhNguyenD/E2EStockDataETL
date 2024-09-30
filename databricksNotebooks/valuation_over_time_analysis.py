# Databricks notebook source
!pip install pyspark

# COMMAND ----------

import pyspark

# COMMAND ----------

import pandas as pd

# COMMAND ----------

from pyspark.sql import SparkSession

# COMMAND ----------

spark = SparkSession.builder.appName('test').getOrCreate()

# COMMAND ----------

spark.conf.set(
    "fs.azure.account.key.xxxxxxx.dfs.core.windows.net",
    "xxxxxxxxxx")

# COMMAND ----------

stage_api_location = "abfss://xxx@xxxxxxxx.dfs.core.windows.net/xxx/"
processed_api_location =  "abfss://xxx@xxxxxxxx.dfs.core.windows.net/xxx/"

# COMMAND ----------

historical_stage_location = stage_api_location + "historicalprice/"
metrics_stage_location = stage_api_location + "keymetrics/"
income_stage_location = stage_api_location + "incomestatement/"

# COMMAND ----------

historical_df = spark.read.option("header", 'true').csv(historical_stage_location)
metrics_df = spark.read.option("header", 'true').csv(metrics_stage_location)
income_df = spark.read.option("header", 'true').csv(income_stage_location)

# COMMAND ----------

from pyspark.sql.functions import year, avg

# Grouping by year (or month/quarter as needed)
grouped_metrics = metrics_df.groupBy(year("date").alias("year")).agg(
    avg("peRatio").alias("avg_peRatio"),
    avg("priceToSalesRatio").alias("avg_priceToSalesRatio"),
    avg("pbRatio").alias("avg_pbRatio"),
    avg("marketCap").alias("avg_marketCap"),
    avg("enterpriseValue").alias("avg_enterpriseValue")
)

# COMMAND ----------

from pyspark.sql import Window
from pyspark.sql.functions import lag

# Define a window specification to calculate year-over-year changes
window = Window.orderBy("year")

# Calculate the year-over-year percentage change for P/E ratio
grouped_metrics = grouped_metrics.withColumn(
    "pe_change", 
    (col("avg_peRatio") - lag("avg_peRatio", 1).over(window)) / lag("avg_peRatio", 1).over(window)
)

# Similarly, calculate the change for other metrics
grouped_metrics = grouped_metrics.withColumn(
    "priceToSales_change", 
    (col("avg_priceToSalesRatio") - lag("avg_priceToSalesRatio", 1).over(window)) / lag("avg_priceToSalesRatio", 1).over(window)
)

grouped_metrics = grouped_metrics.withColumn(
    "marketCap_change", 
    (col("avg_marketCap") - lag("avg_marketCap", 1).over(window)) / lag("avg_marketCap", 1).over(window)
)
grouped_metrics.show()
grouped_metrics.toPandas().plot(x="year", y=["pe_change", "priceToSales_change", "marketCap_change"], kind="line")


# COMMAND ----------

grouped_metrics.write.mode("overwrite").format("parquet").save(processed_api_location + "valuation_analysis/")
