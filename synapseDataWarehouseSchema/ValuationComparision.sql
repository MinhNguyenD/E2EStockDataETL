IF OBJECT_ID('dbo.valuation_comparison', 'U') IS NOT NULL
    DROP TABLE dbo.valuation_comparison;

CREATE TABLE valuation_comparison (
    year INT,
    avg_peRatio FLOAT,
    avg_priceToSalesRatio FLOAT,
    avg_pbRatio FLOAT,
    avg_marketCap FLOAT,
    avg_enterpriseValue FLOAT,
    pe_change FLOAT,
    priceToSales_change FLOAT,
    marketCap_change FLOAT
)
WITH (
    DISTRIBUTION = ROUND_ROBIN,
    HEAP
);
GO