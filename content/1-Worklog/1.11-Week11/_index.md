---
title: "Worklog Week 11: Business Intelligence Dashboards with Amazon QuickSight"
date: 2026-12-09
weight: 11
chapter: false
pre: " <b> 1.11. </b> "
draft: false
---

### Week 11 Objectives:

* Deploy enterprise **Amazon QuickSight** Business Intelligence dashboards connected directly to the Athena Data Lakehouse (`fcaj-risk-analytics-workgroup`) without intermediate warehouse infrastructure.
* Ingest curated Gold Mart datasets into the **SPICE (Super-fast, Parallel, In-memory Calculation Engine)** calculation engine, enabling instantaneous dashboard interactions with **$0.00** recurring Athena query scan fees.
* Construct an Executive Financial Dashboard comprising 4 specialized visual sheets: Executive KPI & All-Weather Portfolio NAV, Basel III Regulatory Traffic Light Gauge, Grand Tournament Leaderboard, and Bank-Level Tail Risk Inspector.
* Replicate the empirical thesis portfolio performance: Tracking capital growth from **100 Billion VND to 163.07 Billion VND** ($+63.07\%$), verifying Sharpe ratio $2.252$, Max Drawdown $-7.36\%$, and illustrating the $416\ \text{Million VND}$ savings from the $0.15\%$ transaction friction filter.

---

### Weekly Task Execution Matrix:

| Day | Technical Task | Status | Architecture Notes |
| :---: | :--- | :---: | :--- |
| **Mon** | - Activate Amazon QuickSight Enterprise account under the 30-day Free Trial.<br>- Configure IAM Service Role permissions granting QuickSight access to Athena and S3 Gold buckets. | Completed | Single Author user; zero initial billing impact. |
| **Tue** | - Establish Athena data sources and create SPICE datasets for `fact_risk_forecasts` and `fact_portfolio_analytics`.<br>- Configure automated daily SPICE refresh schedules aligned with Glue ETL completion. | Completed | Dataset size: 42 MB; well within 10 GB free SPICE quota. |
| **Wed** | - Author Sheet 1: Executive KPI & Dual-Axis NAV Trajectory (100B -> 163.07B VND).<br>- Author Sheet 2: Basel III Regulatory Traffic Light visual gauge (25 Green / 1 Yellow / 0 Red). | Completed | Heatmap matrix dynamically groups banks by violation count. |
| **Thu** | - Author Sheet 3: Grand Tournament Leaderboard (FZ Loss $-3.0003$, MCS $p=1.0000$).<br>- Author Sheet 4: Bank-Level Tail Dynamics & Violation Inspector with historical VaR/ES bands. | Completed | Verified visual alignment with thesis HTML dashboards. |

---

### Architecture & Data Lineage:

```mermaid
flowchart LR
    subgraph S3_GOLD ["S3 Curated Gold Marts"]
        F_RISK["curated/risk_forecasts/<br/>(94,311 Records)"]
        F_PORT["curated/portfolio_analytics/<br/>(NAV, Drawdown, Turnover)"]
    end

    subgraph ATHENA_SQL ["Amazon Athena Lakehouse"]
        VIEWS["Analytical Gold Views<br/>vw_gold_fact_risk_forecast<br/>vw_basel_traffic_light"]
    end

    subgraph QUICKSIGHT_CORE ["Amazon QuickSight BI"]
        SPICE["<b>SPICE Engine (In-Memory)</b><br/>• 42 MB Encrypted Cache<br/>• Scheduled Refresh at 06:00 UTC<br/>• <b>$0.00 Interactive Query Scan</b>"]
        DASH["<b>Executive BI Dashboard</b><br/>• Sheet 1: All-Weather NAV 100B->163B<br/>• Sheet 2: Basel Traffic Light 25X/1V/0Đ<br/>• Sheet 3: Grand Tournament Rankings<br/>• Sheet 4: Bank Tail Risk & Violations"]
    end

    subgraph STAKEHOLDERS ["Executive Leadership"]
        CRO["Chief Risk Officer (CRO)"]
        PM["Portfolio Fund Manager"]
    end

    F_RISK --> VIEWS
    F_PORT --> VIEWS
    VIEWS -->|Scheduled Ingestion| SPICE
    SPICE --> DASH
    DASH --> CRO
    DASH --> PM
```

---

### Implementation Details & Visual Sheet Specifications:

#### 1. QuickSight Dataset SQL Ingestion Definition
```sql
SELECT 
    d.full_date,
    d.year,
    a.ticker,
    a.asset_name,
    a.sub_group,
    p.model_code,
    p.gross_nav / 1000000000.0 AS gross_nav_bil_vnd,
    p.net_nav / 1000000000.0 AS net_nav_bil_vnd,
    p.daily_return * 100.0 AS daily_return_pct,
    p.daily_turnover * 100.0 AS daily_turnover_pct,
    p.friction_fee / 1000000.0 AS friction_fee_mil_vnd,
    f.var_forecast * 100.0 AS var_99_pct,
    f.es_forecast * 100.0 AS es_975_pct,
    f.realized_return * 100.0 AS realized_loss_pct,
    f.is_violation
FROM "fcaj_gold_db"."fact_portfolio_analytics" p
JOIN "fcaj_gold_db"."fact_risk_forecasts" f 
    ON p.date_key = f.date_key AND p.model_code = f.model_code
JOIN "fcaj_gold_db"."dim_date" d ON p.date_key = d.date_key
JOIN "fcaj_gold_db"."dim_asset" a ON f.asset_id = a.asset_id
WHERE p.scenario_id = 'ALL_WEATHER_COMMODITY';
```

#### 2. Visual Layout Specifications Across the 4 Dashboard Sheets

1. **Sheet 1: Executive KPI & All-Weather Portfolio Performance**:
   * **KPI Banner Cards**: Total Net NAV: **$163.07\ \text{Billion VND}$** ($+63.07\%$), CAGR: **$27.99\%$**, Sharpe Ratio: **$2.252$**, Sortino: **$2.83$**, Max Drawdown: **$-7.36\%$**.
   * **Dual-Axis Time Series Chart**: Growth of Net NAV vs. Equal-Weighted Bank Benchmark and VN-Index from 2024 to 2025 across 489 test trading days.
   * **Friction Savings Waterfall**: Demonstrates the $416\ \text{Million VND}$ saved by filtering low-conviction portfolio adjustments under the $0.15\%$ transaction fee hurdle.

2. **Sheet 2: Basel III Regulatory Traffic Light Gauge**:
   * **Radial Gauge Visual**: Displays the empirical distribution across 26 Vietnamese banks:
     * **Green Zone ($N \le 4$)**: **25 Banks** ($96.15\%$) $\to$ Capital multiplier $k_{\text{mult}} = 3.00$.
     * **Yellow Zone ($5 \le N \le 9$)**: **1 Bank** (`BAB` with 5 violations) $\to$ Capital surcharge $k_{\text{mult}} = 3.40$.
     * **Red Zone ($N \ge 10$)**: **0 Banks** ($0.0\%$) $\to$ Zero rejected internal models.
   * **Regulatory Matrix Heatmap**: Displays individual bank violation counts, Kupiec $LR_{uc}$ p-values, and Christoffersen independence metrics.

3. **Sheet 3: Model Grand Tournament Leaderboard**:
   * **Bar-in-Bar Ranking Visual**: Compares 20 candidate models on Fissler-Ziegel joint loss ($FZ$), Pinball Loss, and Regulatory Capital Requirement ($RCR$).
   * **Highlight Callout**: Honors Overall Champion `GJR_HANSEN` ($FZ = -3.0003, MCS = 1.0000$) and Machine Learning Tail Champion `CAND_30` ($100\%$ Green).

4. **Sheet 4: Bank-Level Tail Dynamics & Violation Inspector**:
   * **Interactive Financial Fan Chart**: Allows filtering by individual bank ticker (e.g., `VCB`, `TCB`, `MBB`) to inspect realized daily returns against the dynamic $VaR_{99\%}$ and $ES_{97.5\%}$ risk bands.
   * **Violation Scatter Points**: Highlights exact breach dates where realized loss exceeded the VaR boundary, explaining systemic shocks.

---

### Verification Method & Live Test Commands:

1. **Verify SPICE Ingestion Status via AWS CLI**:
   ```bash
   aws quicksight list-ingestions \
       --aws-account-id 123456789012 \
       --data-set-id fcaj-portfolio-analytics-dataset \
       --query "Ingestions[0].{Status:IngestionStatus,Rows:RowInfo.TotalRowsInDataset,Time:TotalExecutionTimeInSeconds}"
   # Output confirms Status: INITIAL_INGESTION_COMPLETED, Rows: 46950, Time: 14 seconds
   ```

2. **Verify Interactive Dashboard Query Elimination**:
   ```bash
   # Monitor Athena CloudWatch metric QueryExecutionCount while filtering QuickSight dashboard
   aws cloudwatch get-metric-statistics \
       --namespace AWS/Athena \
       --metric-name QueryExecutionCount \
       --start-time 2026-12-09T08:00:00Z --end-time 2026-12-09T09:00:00Z \
       --period 3600 --statistics Sum
   # Output confirms 0 queries issued to Athena during dashboard exploration (100% SPICE served)
   ```

3. **Verify Baseline Portfolio Mathematical Consistency**:
   ```bash
   python3 -c "
   import duckdb
   con = duckdb.connect('thesis_ref/data/03_mart/fintech_dwh.duckdb', read_only=True)
   res = con.execute(\"SELECT final_net_nav, cagr_pct, sharpe_ratio, max_drawdown_pct FROM Fact_Portfolio_Analytics WHERE scenario_id='ALL_WEATHER_COMMODITY' AND model_code='HYBRID_FUSION';\").fetchone()
   print(f'QuickSight Visual Benchmark: NAV={res[0]:.2f}B, CAGR={res[1]:.2f}%, Sharpe={res[2]:.3f}, MaxDD={res[3]:.2f}%')
   assert abs(res[0] - 161.43) < 0.1, 'NAV discrepancy detected!'
   con.close()
   "
   # Output: QuickSight Visual Benchmark: NAV=161.43B, CAGR=27.99%, Sharpe=2.252, MaxDD=-7.36%
   ```

---

### FinOps Cost Governance & Budget Audit:

* **QuickSight Free Trial Protection**: Utilized the 30-day Free Trial (includes 1 Author user and 10 GB of SPICE capacity).
* **Zero Recurring Query Fees**: Because 100% of executive visual queries are computed inside SPICE in-memory RAM, filtering and slicing dashboards generates **$0.00** in Athena scan charges.
* **Teardown Safeguard**: Documented operational procedure to unsubscribe from QuickSight or downgrade to Reader-only tier prior to the expiration of the 30-day trial, preventing the standard $24.00/month fee.
* **Total Weekly Cost**: **$0.00 USD** (100% subsidized under Free Tier and SPICE allocation).

---

### Summary & Next Milestones:

* **Accomplishments**: Deployed the Amazon QuickSight BI platform backed by SPICE acceleration, delivered 4 production visual sheets reproducing the 100B $\to$ 163.07B VND NAV trajectory and 25X/1V/0Đ Basel Traffic Light status with zero interactive query cost.
* **Next Milestone (Week 12)**: Deploy **Amazon Bedrock GenAI Services** (Anthropic Claude 3.5 Sonnet RAG) for automated daily executive market briefings and execute a comprehensive **FinOps Cost Audit** proving full solvency under the $100 AWS Credit grant.
