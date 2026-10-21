---
title: "Week 4 Worklog"
date: 2026-10-21
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
draft: false
---

### Week 4 Objectives:

* Architect and provision a resilient Multi-AZ Custom Amazon Virtual Private Cloud (VPC) aligned with AWS Well-Architected Framework standards.
* Establish scientific CIDR block partitioning for a tiered network topology featuring 2 Public Subnets and 2 Private Subnets.
* Configure Internet Gateway (`ASG-IGW`) and Public Route Tables supporting automatic Public IPv4 assignment.
* Implement private routing domains and integrate FinOps cost guardrails for advanced networking services (NAT Gateway, Site-to-Site VPN).

---

### Tasks Executed During the Week:

| Day | Task Description | Status | Technical Notes |
| :---: | :--- | :---: | :--- |
| **Mon** | - Partitioned `10.10.0.0/16` CIDR block for Custom VPC `ASG`.<br>- Automated Multi-AZ VPC and 4 Subnets provisioning via CloudFormation template `iac/week4-vpc-core.yaml`. | Completed | VPC ID: `vpc-0192f88a9d299fc9b`. |
| **Tue** | - Attached Internet Gateway `ASG-IGW` to VPC.<br>- Configured `ASG-Public-RT` with default route `0.0.0.0/0` targeted to Internet Gateway.<br>- Enabled `MapPublicIpOnLaunch` across both Public Subnets. | Completed | `igw-040b1ff36a17f6e15` (Active). |
| **Wed** | - Configured isolated route table `ASG-Private-RT` for Private Subnets.<br>- Built FinOps guardrail strategy: On-demand ephemeral NAT Gateway provisioning with automated teardown. | Completed | Script `scripts/cleanup_week4_vpc.ps1`. |
| **Thu** | - Researched hybrid connectivity architecture for Site-to-Site VPN using Libreswan on Amazon Linux 2023 (`03-vpc-site-to-site-vpn`).<br>- Formulated secure instance management using AWS Systems Manager (SSM Session Manager) eliminating SSH port 22 exposure. | Completed | Zero open ports posture. |

---

### Step-by-Step Implementation & Technical Evidence:

#### 1. CIDR Subnetting Plan
The network architecture is allocated across a `/16` CIDR block spanning two distinct Availability Zones (`us-east-1a` and `us-east-1b`):

| Subnet Identifier | Availability Zone | CIDR Block | Tier | Auto-Assign Public IP |
| :--- | :---: | :---: | :---: | :---: |
| `ASG-Public-Subnet-1` | `us-east-1a` | `10.10.1.0/24` | Public | **True** |
| `ASG-Public-Subnet-2` | `us-east-1b` | `10.10.2.0/24` | Public | **True** |
| `ASG-Private-Subnet-1` | `us-east-1a` | `10.10.3.0/24` | Private | **False** |
| `ASG-Private-Subnet-2` | `us-east-1b` | `10.10.4.0/24` | Private | **False** |

---

#### 2. Infrastructure-as-Code Automation with CloudFormation
The core network stack is encapsulated declaratively in `iac/week4-vpc-core.yaml` (100% free of charge):

```powershell
aws cloudformation deploy `
    --template-file iac/week4-vpc-core.yaml `
    --stack-name fcaj-week4-vpc `
    --profile fcaj-admin
```
Outcome confirmed: `Successfully created/updated stack - fcaj-week4-vpc`.

![Custom VPC Creation on AWS Console](/images/1-Worklog/1.4-Week4/01_create_custom_vpc.png)

![Multi-AZ Subnets Architecture](/images/1-Worklog/1.4-Week4/02_subnets_multi_az.png)

---

#### 3. AWS CLI Production Verification

##### A. Verify VPC `ASG` Status
```powershell
aws ec2 describe-vpcs `
    --filters "Name=tag:Name,Values=ASG" `
    --query "Vpcs[0].[VpcId,CidrBlock,State]" `
    --output table `
    --profile fcaj-admin
```
```text
---------------------------
|      DescribeVpcs       |
+-------------------------+
|  vpc-0192f88a9d299fc9b  |
|  10.10.0.0/16           |
|  available              |
+-------------------------+
```

##### B. Verify 4 Multi-AZ Subnets
```powershell
aws ec2 describe-subnets `
    --filters "Name=vpc-id,Values=vpc-0192f88a9d299fc9b" `
    --query "Subnets[*].[SubnetId,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch,Tags[?Key=='Name'].Value|[0]]" `
    --output table `
    --profile fcaj-admin
```
```text
---------------------------------------------------------------------------------------------
|                                      DescribeSubnets                                      |
+---------------------------+-------------+---------------+--------+------------------------+
|  subnet-01d4933ac418e0b6a |  us-east-1b |  10.10.4.0/24 |  False |  ASG-Private-Subnet-2  |
|  subnet-0dd99457c6d5da2c0 |  us-east-1a |  10.10.3.0/24 |  False |  ASG-Private-Subnet-1  |
|  subnet-0bf9ef1d8b93fa84f |  us-east-1a |  10.10.1.0/24 |  True  |  ASG-Public-Subnet-1   |
|  subnet-02be355e74a63bd3d |  us-east-1b |  10.10.2.0/24 |  True  |  ASG-Public-Subnet-2   |
+---------------------------+-------------+---------------+--------+------------------------+
```

##### C. Verify Internet Gateway and Route Tables
```powershell
aws ec2 describe-internet-gateways `
    --filters "Name=attachment.vpc-id,Values=vpc-0192f88a9d299fc9b" `
    --query "InternetGateways[*].[InternetGatewayId,Attachments[0].State,Tags[?Key=='Name'].Value|[0]]" `
    --output table `
    --profile fcaj-admin
```
```text
---------------------------------------------------
|            DescribeInternetGateways             |
+------------------------+-------------+----------+
|  igw-040b1ff36a17f6e15 |  available  |  ASG-IGW |
+------------------------+-------------+----------+
```

![Internet Gateway Attachment to VPC ASG](/images/1-Worklog/1.4-Week4/03_attach_internet_gateway.png)

![Public Route Table Default Route Configuration](/images/1-Worklog/1.4-Week4/04_route_table_default_route.png)

`ASG-Public-RT` (`rtb-05bf77bf94acbf8b0`) actively routes `0.0.0.0/0` outbound via `igw-040b1ff36a17f6e15`, allowing bi-directional public internet communication for public subnets. Concurrently, `ASG-Private-RT` (`rtb-0a0c944c4d90bfa3d`) enforces complete network isolation for private workloads.

---

#### 4. FinOps Guardrails: Proactive Cost Containment
Services such as **NAT Gateway** (\$0.045/hr) and **Site-to-Site VPN Connections** (\$0.05/hr) incur running hourly fees that deplete credit limits if neglected. The following safeguards are established:
- **Zero-Waste Audits**: Proactively scanning active VPC resources to guarantee zero unmanaged charges:
```powershell
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=vpc-0192f88a9d299fc9b" --profile fcaj-admin
aws ec2 describe-vpn-connections --profile fcaj-admin
```
Confirmed empty returns: `NatGateways: []` and `VpnConnections: []`.

![NAT Gateway Network Topology](/images/1-Worklog/1.4-Week4/05_nat_gateway_architecture.png)

![Secure Remote Access via Systems Manager Session Manager](/images/1-Worklog/1.4-Week4/06_ssm_session_manager.png)

- **Automated Teardown**: An automated cleanup script `.\scripts\cleanup_week4_vpc.ps1` allows instantaneous resource release whenever required.

---

### Key Outcomes in Week 4:

* **Enterprise-Ready Foundation**: Successfully deployed Multi-AZ Custom VPC `ASG` with strict four-subnet security tiering.
* **100% Infrastructure-as-Code**: Entire network topology is automated through CloudFormation, eliminating manual drift.
* **Zero-Cost Operation**: Core infrastructure maintains \$0.00 spend, preserving the \$100 credit pool for upcoming compute and database tracks.
* **Complete Visual Proof**: Embedded 6 real-world Console screenshots and architectural diagrams.
