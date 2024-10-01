# E2EStockDataETL

End-to-end data engineering project that includes full workflow processes. The project is divided into 3 main phases:

- Ingestion stock and finance data from multiple sources to Azure Datalake V2
- Transformation data from ingestion with Apache Spark Notebook in Azure Databricks
- Load processed data to Data Warehouse (Azure Synapse Analytics dedicated SQL pools) to perform analytical analysis

## Ingestion phase

The ingestion phase includes 2 pipelines that ingest data from multiple sources to Azure Datalake

- Ingestion pipeline for Storage from Azure Blob Storage
- Ingestion pipeline for API Consumption from Financial API server
  Both ingestion pipelines are triggered to pull data monthly. The ingestion pipelines have the sources (storage or API) to consume data and the cleansing dataflow to clean and preprocess data.

## Transformation phase

The transformation phase includes 3 pipelines that perform data transformation and prepare data for the following analyses

- Valuation Comparison Across Time Analysis
- Volatility and Risk Analysis
- Profitability and Growth Analysis

The transformation pipelines are implemented with PySpark in the Azure Databricks environment. The process includes creating new data features and aggregating and filtering data.

## Loading phase

The loading phase includes 3 pipelines that load processed data from Azure Data Lake to Azure Synapse Analytics Warehouse (dedicated SQL pools) to perform the following analyses:

- Valuation Comparison Across Time Analysis
- Volatility and Risk Analysis
- Profitability and Growth Analysis
