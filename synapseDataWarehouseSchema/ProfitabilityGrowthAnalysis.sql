IF OBJECT_ID('dbo.ProfitabilityGrowthAnalysis', 'U') IS NOT NULL
    DROP TABLE dbo.ProfitabilityGrowthAnalysis;

CREATE TABLE dbo.ProfitabilityGrowthAnalysis (
    year INT,
    avg_revenue_growth FLOAT,
    avg_net_income_growth FLOAT,
    avg_gross_margin FLOAT,
    avg_operating_margin FLOAT,
    avg_net_profit_margin FLOAT
)
WITH 
(
    DISTRIBUTION = ROUND_ROBIN,
    HEAP
);
GO