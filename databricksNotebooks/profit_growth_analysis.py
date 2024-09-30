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

metrics_stage_location = stage_api_location + "keymetrics/"
income_stage_location = stage_api_location + "incomestatement/"

# COMMAND ----------

metrics_df = spark.read.option("header", 'true').csv(metrics_stage_location)
income_df = spark.read.option("header", 'true').csv(income_stage_location)

# COMMAND ----------

combined_df = metrics_df.join(income_df, on="date", how="inner")


# COMMAND ----------

from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window

# Define a window specification for calculating previous values
window_spec = Window.orderBy("date")

# Calculate revenue and net income growth
growth_df = combined_df.withColumn("Revenue Growth", (col("Revenue") - lag("Revenue").over(window_spec)) / lag("Revenue").over(window_spec) * 100) \
                       .withColumn("Net Income Growth", (col("Net Income") - lag("Net Income").over(window_spec)) / lag("Net Income").over(window_spec) * 100)


# COMMAND ----------

profitability_df = growth_df.withColumn("Gross Margin", col("Gross Profit") / col("Revenue") * 100) \
                             .withColumn("Operating Margin", col("Operating Income") / col("Revenue") * 100) \
                             .withColumn("Net Profit Margin", col("Net Income") / col("Revenue") * 100)


# COMMAND ----------

from pyspark.sql.functions import avg, year

aggregated_df = profitability_df.groupBy(year("date").alias("year")).agg(
    avg("Revenue Growth").alias("Avg Revenue Growth"),
    avg("Net Income Growth").alias("Avg Net Income Growth"),
    avg("Gross Margin").alias("Avg Gross Margin"),
    avg("Operating Margin").alias("Avg Operating Margin"),
    avg("Net Profit Margin").alias("Avg Net Profit Margin")
)


# COMMAND ----------

display(aggregated_df)

# COMMAND ----------

aggregated_df.toPandas().plot(x="year", y=["Avg Revenue Growth", "Avg Net Income Growth", "Avg Gross Margin", "Avg Operating Margin", "Avg Net Profit Margin"], kind="line")


# COMMAND ----------

aggregated_df.write.mode("overwrite").format("parquet").save(processed_api_location + "profit_growth_analysis/")
