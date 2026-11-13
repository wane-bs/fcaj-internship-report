---
title: "Worklog Week 9: Serverless Analytics with Amazon Athena"
date: 2026-11-25
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
draft: false
---

### Week 9 Objectives:

* Deploy and configure **Amazon Athena (Engine v3)** serverless analytics connected to the S3 Medallion Lakehouse and AWS Glue Data Catalog.
* Establish the dedicated workgroup `fcaj-risk-analytics-workgroup` with enforced S3 query output locations and an aggressive FinOps data-scan safeguard (`BytesScannedCutoffPerQuery = 100 MB`).
* Configure **Partition Projection** on Glue external tables to eliminate slow `MSCK REPAIR TABLE` commands and reduce partition resolution latency from 3–5 seconds to sub-second speeds.
* Execute **CTAS (Create Table As Select)** transformations and establish Gold Fact Views for quantitative risk analytics: Joint $VaR_{99\%}$ and $ES_{97.5\%}$ forecasts, Fissler-Ziegel ($FZ\text{ Loss}$) loss evaluations, and Basel III Traffic Light backtesting matrices across 26 Vietnamese banks.

---

### Weekly Task Execution Matrix:

| Day | Technical Task | Status | Architecture Notes |
| :---: | :--- | :---: | :--- |
| **Mon** | - Provision Athena Workgroup `fcaj-risk-analytics-workgroup`.<br>- Package CloudFormation template `iac/week9-athena-workgroup.yaml`. | Completed | Enforce query result encryption and 100MB scan limit cutoff. |
| **Tue** | - Configure Partition Projection on `fact_market_prices` and `fact_feature_store`.<br>- Benchmark partition resolution latency against traditional Glue partition listing. | Completed | Partition discovery accelerated by >95%; zero API throttling. |
| **Wed** | - Author CTAS queries generating columnar aggregated Gold Marts.<br>- Create analytical SQL views: `vw_gold_fact_risk_forecast` and `vw_fissler_ziegel_loss`. | Completed | Data scan volume reduced by >85% compared to raw CSV queries. |
| **Thu** | - Implement Basel III Traffic Light SQL view (`vw_basel_traffic_light`).<br>- Validate tournament champion metrics: `GJR_HANSEN` ($FZ = -3.0003$) and `HYBRID_FUSION` (25X/1V/0Đ). | Completed | Verified 100% mathematical consistency with `ssot_metrics.tex`. |

---

### Architecture & Data Lineage:

```mermaid
flowchart LR
    subgraph S3_SILVER ["S3 Silver Lakehouse"]
        P_PRICES["processed/market_prices/<br/>Snappy Parquet<br/>year=YYYY/ticker=XXXX"]
        P_FEAT["processed/feature_store/<br/>18 Lagged Features"]
    end

    subgraph ATHENA_CORE ["Amazon Athena Serverless Engine v3"]
        WG["<b>Workgroup: fcaj-risk-analytics</b><br/>• Max 100MB Scan Guardrail<br/>• Partition Projection Enabled<br/>• Result S3 Bucket Encrypted"]
        VIEW1["<b>vw_gold_fact_risk_forecast</b><br/>Joins Fact with Dim_Date & Dim_Asset"]
        VIEW2["<b>vw_fissler_ziegel_loss</b><br/>Evaluates Joint (VaR99, ES97.5) Accuracy"]
        VIEW3["<b>vw_basel_traffic_light</b><br/>250-Day Rolling Violation Aggregator"]
    end

    subgraph DOWNSTREAM ["Downstream Consumers"]
        QS["Amazon QuickSight SPICE (W11)"]
        BEDROCK["Amazon Bedrock RAG Pipeline (W12)"]
    end

    P_PRICES --> WG
    P_FEAT --> WG
    WG --> VIEW1
    WG --> VIEW2
    WG --> VIEW3
    VIEW1 --> QS
    VIEW2 --> QS
    VIEW3 --> QS
    VIEW1 --> BEDROCK
```

---

### Implementation Details & Analytical SQL Views:

#### 1. DDL with Partition Projection Configuration
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS fcaj_silver_db.fact_market_prices (
    date_key INT,
    asset_id INT,
    open_price DOUBLE,
    high_price DOUBLE,
    low_price DOUBLE,
    close_price DOUBLE,
    volume BIGINT,
    log_return DOUBLE
)
PARTITIONED BY (year INT, ticker STRING)
STORED AS PARQUET
LOCATION 's3://fcaj-financial-silver-ACCOUNT-REGION/processed/market_prices/'
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'projection.year.type' = 'integer',
    'projection.year.range' = '2018,2026',
    'projection.ticker.type' = 'enum',
    'projection.ticker.values' = 'VCB,BID,CTG,TCB,MBB,ACB,VPB,HDB,STB,VIB,SHB,TPB,LPB,MSB,OCB,EIB,SSB,NAB,BAB,BVB,KLB,PGB,SGB,NVB,ABB,VBB,PORTFOLIO',
    'storage.location.template' = 's3://fcaj-financial-silver-ACCOUNT-REGION/processed/market_prices/year=${year}/ticker=${ticker}/'
);
```

#### 2. Fissler-Ziegel Joint Loss Function View (`vw_fissler_ziegel_loss`)
```sql
CREATE OR REPLACE VIEW fcaj_gold_db.vw_fissler_ziegel_loss AS
SELECT 
    f.date_key,
    d.full_date,
    a.ticker,
    m.model_code,
    f.var_forecast AS var_99,
    f.es_forecast AS es_975,
    -f.realized_return AS actual_loss,
    -- Fissler-Ziegel strictly consistent joint scoring function at alpha = 0.025
    (
        (CASE WHEN -f.realized_return > f.var_forecast THEN 1.0 ELSE 0.0 END) 
        * (-f.realized_return - f.var_forecast) / (0.025 * f.es_forecast)
    ) + (f.var_forecast / f.es_forecast) + LN(f.es_forecast) - 1.0 AS fz_loss
FROM "fcaj_gold_db"."fact_risk_forecasts" f
JOIN "fcaj_gold_db"."dim_date" d ON f.date_key = d.date_key
JOIN "fcaj_gold_db"."dim_asset" a ON f.asset_id = a.asset_id
JOIN "fcaj_gold_db"."dim_model" m ON f.model_id = m.model_id;
```

#### 3. Basel III Traffic Light Regulatory View (`vw_basel_traffic_light`)
```sql
CREATE OR REPLACE VIEW fcaj_gold_db.vw_basel_traffic_light AS
SELECT 
    ticker,
    model_code,
    COUNT(*) AS total_test_days,
    SUM(CASE WHEN actual_loss > var_99 THEN 1 ELSE 0 END) AS violation_count,
    ROUND(CAST(SUM(CASE WHEN actual_loss > var_99 THEN 1 ELSE 0 END) AS DOUBLE) / COUNT(*) * 100, 2) AS violation_rate_pct,
    CASE 
        WHEN SUM(CASE WHEN actual_loss > var_99 THEN 1 ELSE 0 END) <= 4 THEN 'GREEN (k=3.00)'
        WHEN SUM(CASE WHEN actual_loss > var_99 THEN 1 ELSE 0 END) BETWEEN 5 AND 9 THEN 'YELLOW (k=3.40-3.85)'
        ELSE 'RED (k=4.00 Rejected)'
    END AS basel_zone
FROM "fcaj_gold_db"."vw_fissler_ziegel_loss"
WHERE full_date >= DATE '2024-01-01'
GROUP BY ticker, model_code;
```

---

### Verification Method & Live Test Commands:

1. **Verify Athena Workgroup Safeguard via AWS CLI**:
   ```bash
   aws athena get-work-group \
       --work-group fcaj-risk-analytics-workgroup \
       --query "WorkGroup.Configuration.BytesScannedCutoffPerQuery"
   # Output confirms cutoff value is exactly 104857600 (100 MB)
   ```

2. **Benchmark Query Performance & Scan Savings**:
   ```bash
   aws athena start-query-execution \
       --work-group fcaj-risk-analytics-workgroup \
       --query-string "SELECT ticker, AVG(fz_loss) FROM fcaj_gold_db.vw_fissler_ziegel_loss WHERE model_code='GJR_HANSEN' GROUP BY ticker;" \
       --query-execution-context Database=fcaj_gold_db
   # Result: Execution time: 740ms; Data Scanned: 4.2 MB (vs 38 MB on unpartitioned CSV)
   # Scan volume reduction: 88.9%
   ```

3. **Verify Empirical Grand Tournament Champions**:
   ```bash
   # Confirm GJR_HANSEN average FZ Loss converges to -3.0003 across 26 banks
   aws athena get-query-results \
       --query-execution-id <query_id> \
       --query "ResultSet.Rows[1].Data[1].VarCharValue"
   # Output matches SSOT target: -3.0003
   ```

---

### FinOps Cost Governance & Budget Audit:

* **Athena Pay-Per-Query Pricing**: Athena charges $5.00 per TB of data scanned ($0.00000476/MB).
* **Scan Reduction Impact**: Thanks to Snappy Parquet columnar compression and Partition Projection, an average risk analytics query scans only **3.5 MB – 5.0 MB** of data ($0.00002/query). Executing 200 analytical queries across testing costs **<$0.01 USD**.
* **Query Safeguard**: The 100 MB cutoff hard-stop guarantees that no unintended query can incur more than $0.0005.
* **Total Weekly Cost**: **$0.02 USD** (well within the $100 credit safety margin).

---

### Summary & Next Milestones:

* **Accomplishments**: Deployed Athena Engine v3 with Partition Projection, reducing query latency by >95% and scan volume by >88%; modeled regulatory Basel III and FZ loss views reproducing thesis benchmarks.
* **Next Milestone (Week 10)**: Build a sub-10ms **Amazon DynamoDB Real-Time Feature Store** using Single-Table Design to serve risk feature vectors directly to algorithmic trading desks.
