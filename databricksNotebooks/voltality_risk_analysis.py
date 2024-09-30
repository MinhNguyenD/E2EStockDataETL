# Databricks notebook source
import pyspark
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('test').getOrCreate()
spark.conf.set(
    "fs.azure.account.key.xxxxxxx.dfs.core.windows.net",
    "xxxxxxxxxx")

# COMMAND ----------

stage_api_location = "abfss://xxx@xxxxxxxx.dfs.core.windows.net/xxx/"
processed_api_location =  "abfss://xxx@xxxxxxxx.dfs.core.windows.net/xxx/"

# COMMAND ----------

historical_stage_location = stage_api_location + "historicalprice/"
quote_stage_location = stage_api_location + "quote/"

# COMMAND ----------

historical_df = spark.read.option("header", 'true').csv(historical_stage_location)
quote_df = spark.read.option("header", 'true').csv(quote_stage_location)

# COMMAND ----------

from pyspark.sql import functions as F

# Calculate daily returns
returns_df = historical_df.select(
    "symbol",
    ((F.col("close") - F.col("open")) / F.col("open")).alias("daily_return"),
    "date"
)


# COMMAND ----------

# Join quote data with daily returns
joined_df = returns_df.join(quote_df, "symbol", "inner")

# COMMAND ----------

# Calculate volatility
volatility_df = joined_df.groupBy("symbol").agg(
    F.stddev("daily_return").alias("volatility"),
    F.avg("marketCap").alias("avg_marketCap"),
    F.avg("pe").alias("avg_pe")
)


# COMMAND ----------

from pyspark.sql import Window

# Assuming a confidence level (e.g., 95%)
confidence_level = 0.95

window = Window.orderBy("symbol")

# Calculate Value at Risk (VaR)
risk_df = volatility_df.withColumn("VaR", F.expr(f"percentile(volatility, {confidence_level})").over(window))


# COMMAND ----------

display(risk_df)


# COMMAND ----------

risk_df.write.mode("overwrite").format("parquet").save(processed_api_location + "voltality_risk_analysis/")
