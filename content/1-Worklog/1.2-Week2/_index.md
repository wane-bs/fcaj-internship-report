---
title: "Week 2 Worklog"
date: 2026-10-07
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
draft: false
---

### Week 2 Objectives:

* Implement Day 0 Security & FinOps Guardrails for the newly created AWS account.
* Deploy modern identity management using **IAM Identity Center (AWS SSO)** to eliminate dangerous static Access Keys.
* Set up financial barriers (**AWS Budgets**) and comprehensive audit monitoring (**AWS CloudTrail**).
* Integrate the local development environment and Antigravity IDE with **AWS CLI v2**, **AWS Agent Toolkit**, and **AWS MCP Server**.

---

### Tasks completed this week:

| Day | Task | Status | Technical Details |
| :---: | :--- | :---: | :--- |
| **Mon** | - Create personal AWS account (`658302145298`).<br>- Enable Multi-Factor Authentication (MFA) for the Root user.<br>- Install AWS CLI v2 on Windows. | Completed | Protected via Authenticator App. |
| **Tue** | - Integrate the AI assistant suite with **AWS Agent Toolkit** and load **AWS Skill Pack** (`pack-aws` featuring 24 specialized skills).<br>- Configure the official SigV4-compliant **AWS MCP Server** (`aws-mcp`) in Antigravity IDE.<br>- Resolve and standardize Windows `PATH` for `aws.exe`. | Completed | 8 dedicated MCP tools & 24 AWS domain skills configured. |
| **Wed** | - Set up 2-tier financial alerts via **AWS Budgets**:<br>&emsp;+ Zero-Spend budget (`$0.01/month`) for instant resource leak detection.<br>&emsp;+ Monthly learning budget (`$5.00/month`) with forecasted alarm.<br>- Route alert notifications to `01134wane@gmail.com`. | Completed | Created via automated CLI input. |
| **Thu** | - Configure **AWS CloudTrail** security audit logging (Multi-Region):<br>&emsp;+ Create dedicated S3 Bucket with 100% Block Public Access.<br>&emsp;+ Enable Log File Validation. | Completed | `fcaj-management-events-trail` (`IsLogging: True`). |
| **Fri** | - Enable **IAM Identity Center (AWS SSO)** in region `us-east-1`.<br>- Create admin user `hieu-admin` and assign `AdministratorAccess` permission set.<br>- Configure CLI profile `fcaj-admin` via Web SSO Login flow.<br>- Isolate and lock Root credentials (zero static keys). | Completed | Authenticated using temporary STS credentials. |

---

### Implementation Details & Evidence:

#### 1. Agent Toolkit and AWS MCP Server Integration for IDE
To maximize development productivity and automate cloud operations safely from Antigravity IDE:
- Executed `aws configure agent-toolkit` to detect the environment and download all 24 official AWS specialized skills:

![Installing 24 Skills via AWS Agent Toolkit](/images/1-Worklog/1.2-Week2/00_agent_toolkit_install.png)

- **AWS Skill Pack (`pack-aws`)**: Embedded 24 specialized skills under `.agents/skills/` encompassing: Security & Architecture (`aws-iam`, `aws-security`, `aws-well-architected-review`), Cloud Infrastructure (`aws-compute`, `aws-storage`, `aws-networking`, `aws-database`, `aws-serverless`, `aws-containers`), IaC & Automation (`aws-cdk`, `aws-cloudformation`), FinOps (`aws-billing-and-cost-management`), and Generative AI (`amazon-bedrock`, `aws-ai-ml`).
- **AWS MCP Server (`aws-mcp`)**: Configured the official AWS Model Context Protocol server utilizing AWS SigV4 authentication, exposing 8 direct tools:
  - `aws___run_script`: Securely executes AWS commands and scripts through MCP sandbox.
  - `aws___get_presigned_url`: Generates secure temporary presigned URLs for S3 transfers.
  - `aws___search_documentation` & `aws___read_documentation`: Retrieves canonical AWS documentation and architectural guidance.
  - `aws___retrieve_skill`: Loads deep technical skill patterns on-demand.
  - `aws___list_regions` & `aws___get_regional_availability`: Inspects regional service availability.
  - `aws___get_tasks`: Manages long-running asynchronous background cloud tasks.
- **Project Routing Rules**: Established `AGENTS.md` in the workspace root to direct AI agents to prefer MCP interactions over bare shell executions.

#### 2. PATH Standardization and Cost Guardrails (AWS Budgets)
To prevent unexpected charges and ensure smooth local terminal workflows:
- Normalized the AWS CLI binary location in the Windows `User PATH` (`C:\Users\FUJITSU\AppData\Local\Programs\AWSCLIV2\Amazon\AWSCLIV2`).
- Created two budget rules using `aws budgets create-budget`:
  - `fcaj-zero-spend-alert`: Triggers when actual spend exceeds 80% of \$0.01.
  - `fcaj-monthly-5usd-budget`: Triggers at \$4.00 actual or \$5.00 forecasted.

#### 3. IAM Identity Center & Permission Set Creation
Rather than using classic IAM Users with permanent credentials stored on disk, modern **AWS SSO** was configured:
- Enabled **IAM Identity Center** under AWS Organizations.
- Created an `AdministratorAccess` Permission Set providing full administrative privileges securely.

![Created AdministratorAccess Permission Set](/images/1-Worklog/1.2-Week2/01_permission_set_created.png)

#### 4. Connecting AWS CLI via Web SSO
Linked the local terminal session using:
```powershell
aws configure sso
```
Supplied the SSO start URL (`https://d-90666396a9.awsapps.com/start`) and region (`us-east-1`):

![Configuring SSO Start URL on Terminal](/images/1-Worklog/1.2-Week2/02_aws_configure_sso_start.png)

#### 5. Account and Role Selection
The system automatically mapped user `hieu-admin` to account `658302145298` with the `AdministratorAccess` role. Assigned CLI profile name as `fcaj-admin`:

![Selecting Account and Admin Role](/images/1-Worklog/1.2-Week2/03_sso_account_role_select.png)

#### 6. Successful Authentication & Secure Session Handoff
Authentication completed successfully in the browser, issuing temporary session tokens to the terminal:

![SSO Login Success](/images/1-Worklog/1.2-Week2/04_sso_login_success.png)

Verifying identity via AWS STS:
```powershell
aws sts get-caller-identity
```
```json
{
    "UserId": "AROAZSRO5SMJCCG7ZP6SR:hieu-admin",
    "Account": "658302145298",
    "Arn": "arn:aws:sts::658302145298:assumed-role/AWSReservedSSO_AdministratorAccess_779cba0fb7efbed6/hieu-admin"
}
```

---

### Week 2 Achievements:

* **Enterprise-Grade Security**: Account fortified with Root MFA, IAM Identity Center SSO, and zero static access keys.
* **Proactive FinOps Protection**: Free Tier limits strictly monitored with instant alerts for any unexpected spend.
* **Transparent Auditing**: All API activities across all regions captured by AWS CloudTrail and encrypted in S3.
* **Deep Agent Toolkit & MCP Integration**: Equipped IDE with 24 specialized AWS skills and the official SigV4 MCP Server, empowering AI to assist in architectural reviews, documentation retrieval, and secure cloud operations.
