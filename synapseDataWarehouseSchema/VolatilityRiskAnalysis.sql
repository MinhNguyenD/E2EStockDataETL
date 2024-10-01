IF OBJECT_ID('dbo.VolatilityRiskAnalysis', 'U') IS NOT NULL
    DROP TABLE dbo.VolatilityRiskAnalysis;

CREATE TABLE dbo.VolatilityRiskAnalysis (
    symbol NVARCHAR(10),
    volatility FLOAT,
    avg_marketCap FLOAT,
    avg_pe FLOAT,
    VaR FLOAT
)
WITH 
(
    DISTRIBUTION = ROUND_ROBIN,
    HEAP
);
GO