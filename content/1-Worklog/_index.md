---
title: "Worklog"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 1. </b> "
---

# Internship Worklog

The **Worklog** section documents the weekly learning progress, hands-on tasks, and AWS cloud engineering activities throughout the **First Cloud AI Journey (FCAJ)** internship program.

---

### Weekly Progress & Milestones

* **[Week 1: AWS Account Activation & $100 Credit Verification](1.1-week1/)** `[Completed]`  
  *Activated personal AWS account, verified receipt of $100 AWS Credit, explored AWS Billing & Cost Management Console, and established cost control roadmap.*

* **[Week 2: Day 0 Security & FinOps Guardrails](1.2-week2/)** `[Completed]`  
  *Activated Root MFA, configured IAM Identity Center (AWS SSO), established dual AWS Budgets alarms, enabled CloudTrail audit trails, and integrated AWS MCP Server / Agent Toolkit.*

* **[Week 3: IAM Access Governance & STS Role Switching](1.3-week3/)** `[Completed]`  
  *Implemented Least Privilege governance, automated AdminGroup, AdminRole, and OperatorUser via CloudFormation, and validated temporary credential elevation via AWS STS AssumeRole.*

* **[Week 4: Isolated Multi-AZ Custom VPC Architecture](1.4-week4/)** `[Completed]`  
  *Partitioned `10.10.0.0/16` CIDR block, provisioned Custom VPC `ASG` with 4 Multi-AZ subnets, configured Internet Gateway, Route Tables, and zero-cost FinOps controls.*

* **[Week 5: Amazon EC2 Linux Administration & EBS Storage](1.5-week5/)** `[Planned]`  
  *Administer EC2 Linux compute, bootstrap instances via User Data, manage persistent EBS volumes, and produce golden Custom AMIs.*

* **[Week 6: Amazon RDS PostgreSQL Relational Databases](1.6-week6/)** `[Planned]`  
  *Deploy RDS PostgreSQL Multi-AZ High Availability clusters, configure Read Replicas, and rotate secrets via AWS Secrets Manager.*

* **[Week 7: S3 Data Lake Foundation & VPC Endpoints](1.7-week7/)** `[Planned]`  
  *Architect tiered S3 Data Lake (Raw, Processed, Curated) and implement zero-cost S3 Gateway VPC Endpoints for private traffic.*

* **[Week 8: Automated Data Pipelines with AWS Glue](1.8-week8/)** `[Planned]`  
  *Catalog metadata via Glue Crawlers, manage Glue Data Catalog, and build visual serverless ETL Parquet conversion pipelines with Glue Studio.*

* **[Week 9: Serverless Analytics with Amazon Athena](1.9-week9/)** `[Planned]`  
  *Execute interactive Serverless SQL analytics, benchmark query execution, and optimize costs using CTAS and data partitioning.*

* **[Week 10: High-Throughput NoSQL with Amazon DynamoDB](1.10-week10/)** `[Planned]`  
  *Design NoSQL single-table patterns, configure Global Secondary Indexes (GSI), and execute batch operations with Python Boto3 SDK.*

* **[Week 11: Business Intelligence Dashboards with Amazon QuickSight](1.11-week11/)** `[Planned]`  
  *Ingest data from Athena into SPICE in-memory acceleration engine and publish interactive executive BI dashboards.*

* **[Week 12: Machine Learning with Amazon SageMaker & Final Capstone](1.12-week12/)** `[Planned]`  
  *Train and deploy XGBoost predictive model via SageMaker Studio, execute resource teardown, and finalize comprehensive internship showcase.*

---

> [!NOTE]
> Progress entries are updated continuously along the internship implementation milestones, aligned with AWS Well-Architected Framework principles.
