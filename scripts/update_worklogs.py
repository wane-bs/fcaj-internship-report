import os

content_dir = r"d:\DebianBackup\source_code\fcaj\content\1-Worklog"

# Define realistic curriculum roadmaps for Weeks 3 to 12
weeks_data = [
    {
        "num": 3,
        "title_vi": "Worklog Tuần 3",
        "title_en": "Week 3 Worklog",
        "weight": 3,
        "date": "2026-10-14",
        "obj_vi": ["Nắm vững kiến trúc quản trị danh tính và kiểm soát truy cập với AWS IAM.", "Thực hành cấu hình IAM User, Group, Customer Managed Policy và Role Switching."],
        "obj_en": ["Master identity governance and access control with AWS IAM.", "Configure IAM Users, Groups, Customer Managed Policies, and Cross-Role Switching."],
        "tasks_vi": [
            ("2", "Nghiên cứu nguyên tắc Least Privilege và cấu trúc IAM Policy JSON chuẩn", "13/10/2026", "13/10/2026", "02-iam-security"),
            ("3", "Thực hành tạo Admin Group, gán quyền và tạo OperatorUser giới hạn", "14/10/2026", "14/10/2026", "02-iam-security"),
            ("4", "Thiết lập Role Switching cho OperatorUser để nâng quyền tạm thời qua STS", "15/10/2026", "15/10/2026", "02-iam-security"),
            ("5", "Kiểm thử phân quyền và đánh giá nhật ký đăng nhập IAM", "16/10/2026", "16/10/2026", "02-iam-security")
        ],
        "tasks_en": [
            ("Mon", "Study Least Privilege principles and standard IAM Policy JSON structure", "10/13/2026", "10/13/2026", "02-iam-security"),
            ("Tue", "Create Admin Group, assign policies, and create restricted OperatorUser", "10/14/2026", "10/14/2026", "02-iam-security"),
            ("Wed", "Configure Role Switching for OperatorUser via temporary STS tokens", "10/15/2026", "10/15/2026", "02-iam-security"),
            ("Thu", "Verify access permissions and audit IAM authentication events", "10/16/2026", "10/16/2026", "02-iam-security")
        ]
    },
    {
        "num": 4,
        "title_vi": "Worklog Tuần 4",
        "title_en": "Week 4 Worklog",
        "weight": 4,
        "date": "2026-10-21",
        "obj_vi": ["Thiết kế mạng ảo Amazon VPC tùy biến (Custom VPC) với đầy đủ Public/Private Subnets.", "Cấu hình Internet Gateway, NAT Gateway và thiết lập Site-to-Site VPN."],
        "obj_en": ["Design Custom Amazon VPC with isolated Public/Private Subnets.", "Configure Internet Gateway, NAT Gateway, and establish Site-to-Site VPN."],
        "tasks_vi": [
            ("2", "Phân hoạch dải địa chỉ CIDR và tạo VPC đa vùng sẵn sàng (Multi-AZ)", "20/10/2026", "20/10/2026", "03-vpc-site-to-site-vpn"),
            ("3", "Cấu hình Route Tables, Internet Gateway cho Public Subnet", "21/10/2026", "21/10/2026", "03-vpc-site-to-site-vpn"),
            ("4", "Triển khai NAT Gateway cho Private Subnet và kiểm tra kết nối outbound", "22/10/2026", "22/10/2026", "03-vpc-site-to-site-vpn"),
            ("5", "Thực hành lab mô phỏng Site-to-Site VPN kết nối môi trường giả lập on-premises", "23/10/2026", "23/10/2026", "03-vpc-site-to-site-vpn")
        ],
        "tasks_en": [
            ("Mon", "Plan CIDR blocks and deploy Multi-AZ Custom VPC", "10/20/2026", "10/20/2026", "03-vpc-site-to-site-vpn"),
            ("Tue", "Configure Route Tables and Internet Gateway for Public Subnets", "10/21/2026", "10/21/2026", "03-vpc-site-to-site-vpn"),
            ("Wed", "Provision NAT Gateway for Private Subnets and test outbound connectivity", "10/22/2026", "10/22/2026", "03-vpc-site-to-site-vpn"),
            ("Thu", "Execute Site-to-Site VPN simulation lab connecting mock on-premise network", "10/23/2026", "10/23/2026", "03-vpc-site-to-site-vpn")
        ]
    },
    {
        "num": 5,
        "title_vi": "Worklog Tuần 5",
        "title_en": "Week 5 Worklog",
        "weight": 5,
        "date": "2026-10-28",
        "obj_vi": ["Quản trị điện toán Amazon EC2, EBS Storage Volumes và tự động hóa qua User Data.", "Thực hành xử lý sự cố mất Key Pair trên cả môi trường Linux và Windows."],
        "obj_en": ["Administer Amazon EC2 compute, EBS Volumes, and automate bootstrap via User Data.", "Troubleshoot Key Pair loss on both Linux and Windows environments."],
        "tasks_vi": [
            ("2", "Khởi tạo EC2 Linux, cấu hình LAMP stack tự động qua EC2 User Data", "27/10/2026", "27/10/2026", "04-ec2-linux-admin"),
            ("3", "Thực hành gắn thêm EBS Volume, định dạng filesystem và cấu hình mount tự động", "28/10/2026", "28/10/2026", "04-ec2-linux-admin"),
            ("4", "Mô phỏng và xử lý sự cố mất Key Pair: Dùng User Data trên Linux, SSM trên Windows", "29/10/2026", "29/10/2026", "04-ec2-linux-admin"),
            ("5", "Tạo Custom AMI và kiểm tra quy trình nhân bản máy chủ", "30/10/2026", "30/10/2026", "04-ec2-linux-admin")
        ],
        "tasks_en": [
            ("Mon", "Launch EC2 Linux and automate LAMP stack via EC2 User Data", "10/27/2026", "10/27/2026", "04-ec2-linux-admin"),
            ("Tue", "Attach EBS Volume, format filesystem, and configure persistent fstab mounting", "10/28/2026", "10/28/2026", "04-ec2-linux-admin"),
            ("Wed", "Troubleshoot lost Key Pair recovery: User Data for Linux, SSM for Windows", "10/29/2026", "10/29/2026", "04-ec2-linux-admin"),
            ("Thu", "Create Custom AMI and validate golden image reproduction", "10/30/2026", "10/30/2026", "04-ec2-linux-admin")
        ]
    },
    {
        "num": 6,
        "title_vi": "Worklog Tuần 6",
        "title_en": "Week 6 Worklog",
        "weight": 6,
        "date": "2026-11-04",
        "obj_vi": ["Khởi tạo và quản trị cơ sở dữ liệu quan hệ Amazon RDS PostgreSQL chuyên sâu.", "Thiết lập cấu hình Multi-AZ High Availability và Read Replica."],
        "obj_en": ["Provision and manage Amazon RDS PostgreSQL relational databases.", "Configure Multi-AZ High Availability and Read Replica architectures."],
        "tasks_vi": [
            ("2", "Triển khai RDS PostgreSQL instance trong Private Subnet", "03/11/2026", "03/11/2026", "20-rds-postgresql-part1"),
            ("3", "Thiết lập Multi-AZ Deployment và thử nghiệm failover tự động", "04/11/2026", "04/11/2026", "20-rds-postgresql-part1"),
            ("4", "Cấu hình Read Replica để giảm tải truy vấn đọc và mở rộng hiệu năng", "05/11/2026", "05/11/2026", "20-rds-postgresql-part1"),
            ("5", "Tích hợp AWS Secrets Manager để tự động xoay vòng mật khẩu database", "06/11/2026", "06/11/2026", "21-rds-postgresql-part2")
        ],
        "tasks_en": [
            ("Mon", "Deploy RDS PostgreSQL instance in isolated Private Subnet", "11/03/2026", "11/03/2026", "20-rds-postgresql-part1"),
            ("Tue", "Configure Multi-AZ Deployment and test automated failover", "11/04/2026", "11/04/2026", "20-rds-postgresql-part1"),
            ("Wed", "Set up Read Replicas for read-workload offloading and scale", "11/05/2026", "11/05/2026", "20-rds-postgresql-part1"),
            ("Thu", "Integrate AWS Secrets Manager for automated database credential rotation", "11/06/2026", "11/06/2026", "21-rds-postgresql-part2")
        ]
    },
    {
        "num": 7,
        "title_vi": "Worklog Tuần 7",
        "title_en": "Week 7 Worklog",
        "weight": 7,
        "date": "2026-11-11",
        "obj_vi": ["Bắt đầu Track Data & Analytics: Xây dựng nền tảng Data Lake trên Amazon S3.", "Ứng dụng VPC Endpoints để tối ưu chi phí và tăng cường an toàn dữ liệu."],
        "obj_en": ["Begin Data & Analytics Track: Build foundational Data Lake on Amazon S3.", "Implement VPC Endpoints to eliminate NAT Gateway fees and isolate data."],
        "tasks_vi": [
            ("2", "Quy hoạch kiến trúc Data Lake S3: Phân tầng Raw, Processed, Curated Zones", "10/11/2026", "10/11/2026", "10-datalake-basics"),
            ("3", "Cấu hình S3 Gateway VPC Endpoint loại bỏ phí NAT Gateway", "11/11/2026", "11/11/2026", "14-s3-vpc-endpoints"),
            ("4", "Thiết lập S3 Bucket Policy siết chặt quyền truy cập chỉ từ VPC Endpoint", "12/11/2026", "12/11/2026", "14-s3-vpc-endpoints"),
            ("5", "Đánh giá hiệu quả bảo mật và chi phí sau khi bật Endpoint", "13/11/2026", "13/11/2026", "14-s3-vpc-endpoints")
        ],
        "tasks_en": [
            ("Mon", "Architect S3 Data Lake: Zone partitioning for Raw, Processed, and Curated tiers", "11/10/2026", "11/10/2026", "10-datalake-basics"),
            ("Tue", "Deploy S3 Gateway VPC Endpoint to eliminate NAT Gateway data processing fees", "11/11/2026", "11/11/2026", "14-s3-vpc-endpoints"),
            ("Wed", "Enforce S3 Bucket Policy restricting traffic exclusively via VPC Endpoint", "11/12/2026", "11/12/2026", "14-s3-vpc-endpoints"),
            ("Thu", "Audit network logs and verify zero-cost private access", "11/13/2026", "11/13/2026", "14-s3-vpc-endpoints")
        ]
    },
    {
        "num": 8,
        "title_vi": "Worklog Tuần 8",
        "title_en": "Week 8 Worklog",
        "weight": 8,
        "date": "2026-11-18",
        "obj_vi": ["Triển khai luồng ETL tự động với AWS Glue Crawlers và AWS Glue Studio.", "Quản lý siêu dữ liệu tập trung qua AWS Glue Data Catalog."],
        "obj_en": ["Automate ETL pipelines using AWS Glue Crawlers and Glue Studio.", "Centrally manage metadata catalogs via AWS Glue Data Catalog."],
        "tasks_vi": [
            ("2", "Thiết lập Glue Crawler quét dữ liệu thô từ S3 Raw Bucket vào Data Catalog", "17/11/2026", "17/11/2026", "11-custom-datalake"),
            ("3", "Kiểm tra schema phát sinh và xử lý schema evolution", "18/11/2026", "18/11/2026", "11-custom-datalake"),
            ("4", "Tạo Visual ETL Job bằng AWS Glue Studio chuyển đổi dữ liệu sang Parquet", "19/11/2026", "19/11/2026", "11-custom-datalake"),
            ("5", "Thực thi kiểm tra chất lượng dữ liệu với AWS Glue DataBrew", "20/11/2026", "20/11/2026", "11-custom-datalake")
        ],
        "tasks_en": [
            ("Mon", "Configure Glue Crawler to discover raw S3 schemas into Data Catalog", "11/17/2026", "11/17/2026", "11-custom-datalake"),
            ("Tue", "Validate schema discovery and manage partition schema evolution", "11/18/2026", "11/18/2026", "11-custom-datalake"),
            ("Wed", "Build Visual ETL Job in Glue Studio transforming CSV to snappy Parquet", "11/19/2026", "11/19/2026", "11-custom-datalake"),
            ("Thu", "Run profiling and cleaning recipes with AWS Glue DataBrew", "11/20/2026", "11/20/2026", "11-custom-datalake")
        ]
    },
    {
        "num": 9,
        "title_vi": "Worklog Tuần 9",
        "title_en": "Week 9 Worklog",
        "weight": 9,
        "date": "2026-11-25",
        "obj_vi": ["Truy vấn phân tích dữ liệu không máy chủ (Serverless SQL) bằng Amazon Athena.", "Tối ưu hóa chi phí truy vấn thông qua Partitioning và CTAS."],
        "obj_en": ["Perform Serverless SQL interactive analytics using Amazon Athena.", "Optimize Athena query costs and speed via Partitioning and CTAS queries."],
        "tasks_vi": [
            ("2", "Cấu hình Athena Workgroup và vị trí lưu trữ kết quả truy vấn trên S3", "24/11/2026", "24/11/2026", "13-athena-serverless"),
            ("3", "Thực hiện các truy vấn phân tích tổng hợp dữ liệu giao dịch", "25/11/2026", "25/11/2026", "13-athena-serverless"),
            ("4", "Áp dụng câu lệnh CTAS (Create Table As Select) để tạo bảng tối ưu", "26/11/2026", "26/11/2026", "11-custom-datalake"),
            ("5", "Đo lường dung lượng dữ liệu quét và chi phí trước/sau khi tối ưu Parquet", "27/11/2026", "27/11/2026", "12-glue-athena-analytics")
        ],
        "tasks_en": [
            ("Mon", "Configure Athena Workgroup and designated S3 query output location", "11/24/2026", "11/24/2026", "13-athena-serverless"),
            ("Tue", "Run aggregations and analytic SQL queries on partitioned datasets", "11/25/2026", "11/25/2026", "13-athena-serverless"),
            ("Wed", "Apply CTAS queries to repartition datasets into columnar storage", "11/26/2026", "11/26/2026", "11-custom-datalake"),
            ("Thu", "Benchmark scan volumes and cost savings comparing raw CSV vs Parquet", "11/27/2026", "11/27/2026", "12-glue-athena-analytics")
        ]
    },
    {
        "num": 10,
        "title_vi": "Worklog Tuần 10",
        "title_en": "Week 10 Worklog",
        "weight": 10,
        "date": "2026-12-02",
        "obj_vi": ["Lưu trữ dữ liệu phi quan hệ tốc độ cao với Amazon DynamoDB.", "Tích hợp Python Boto3 SDK để thực thi các tác vụ CRUD và truy vấn GSI."],
        "obj_en": ["Implement high-throughput NoSQL storage with Amazon DynamoDB.", "Integrate Python Boto3 SDK for CRUD and Global Secondary Index queries."],
        "tasks_vi": [
            ("2", "Thiết kế Data Model DynamoDB: Partition Key, Sort Key, và On-Demand Capacity", "01/12/2026", "01/12/2026", "15-dynamodb-nosql"),
            ("3", "Viết script Python Boto3 thực hiện Batch Write và Get Item", "02/12/2026", "02/12/2026", "15-dynamodb-nosql"),
            ("4", "Tạo và kiểm thử truy vấn tối ưu qua Global Secondary Index (GSI)", "03/12/2026", "03/12/2026", "15-dynamodb-nosql"),
            ("5", "Đánh giá Read/Write Capacity Modes và bài toán tối ưu chi phí NoSQL", "04/12/2026", "04/12/2026", "15-dynamodb-nosql")
        ],
        "tasks_en": [
            ("Mon", "Design DynamoDB Schema: Partition Key, Sort Key, and On-Demand capacity", "12/01/2026", "12/01/2026", "15-dynamodb-nosql"),
            ("Tue", "Develop Python Boto3 scripts for Batch Write and Get Item operations", "12/02/2026", "12/02/2026", "15-dynamodb-nosql"),
            ("Wed", "Create and benchmark query patterns via Global Secondary Indexes (GSI)", "12/03/2026", "12/03/2026", "15-dynamodb-nosql"),
            ("Thu", "Evaluate Provisioned vs On-Demand capacity cost impact", "12/04/2026", "12/04/2026", "15-dynamodb-nosql")
        ]
    },
    {
        "num": 11,
        "title_vi": "Worklog Tuần 11",
        "title_en": "Week 11 Worklog",
        "weight": 11,
        "date": "2026-12-09",
        "obj_vi": ["Xây dựng Dashboard phân tích trực quan Business Intelligence với Amazon QuickSight.", "Thiết lập kết nối an toàn từ QuickSight đến Amazon Athena."],
        "obj_en": ["Build interactive BI analytics dashboards using Amazon QuickSight.", "Configure secure data ingestion from Amazon Athena into SPICE engine."],
        "tasks_vi": [
            ("2", "Khởi tạo tài khoản QuickSight và cấp quyền truy cập S3 & Athena", "08/12/2026", "08/12/2026", "18-quicksight-bi"),
            ("3", "Tạo Dataset từ Athena Table và cấu hình SPICE In-memory Engine", "09/12/2026", "09/12/2026", "18-quicksight-bi"),
            ("4", "Xây dựng các biểu đồ KPI, Trend Line, Pivot Table và Filter Actions", "10/12/2026", "10/12/2026", "18-quicksight-bi"),
            ("5", "Xuất bản Interactive Dashboard và phân quyền chia sẻ người dùng", "11/12/2026", "11/12/2026", "18-quicksight-bi")
        ],
        "tasks_en": [
            ("Mon", "Set up QuickSight account and grant S3 / Athena service role access", "12/08/2026", "12/08/2026", "18-quicksight-bi"),
            ("Tue", "Build Data Source from Athena and import data into SPICE in-memory engine", "12/09/2026", "12/09/2026", "18-quicksight-bi"),
            ("Wed", "Design KPI widgets, Time-series trend lines, Pivot tables, and Filters", "12/10/2026", "12/10/2026", "18-quicksight-bi"),
            ("Thu", "Publish and share interactive dashboard with role-based governance", "12/11/2026", "12/11/2026", "18-quicksight-bi")
        ]
    },
    {
        "num": 12,
        "title_vi": "Worklog Tuần 12",
        "title_en": "Week 12 Worklog",
        "weight": 12,
        "date": "2026-12-16",
        "obj_vi": ["Ứng dụng Machine Learning trên AWS với Amazon SageMaker.", "Tổng kết toàn bộ chu kỳ thực tập và hoàn thiện hồ sơ dự án."],
        "obj_en": ["Apply Machine Learning on AWS with Amazon SageMaker Immersion Day.", "Synthesize internship report and deliver final portfolio showcase."],
        "tasks_vi": [
            ("2", "Làm quen với Amazon SageMaker Studio và chuẩn bị dataset qua Data Wrangler", "15/12/2026", "15/12/2026", "19-sagemaker-immersion-day"),
            ("3", "Huấn luyện và tinh chỉnh mô hình XGBoost dự đoán trên dữ liệu phân tích", "16/12/2026", "16/12/2026", "19-sagemaker-immersion-day"),
            ("4", "Deploy Endpoint mô hình và thực hiện suy luận dự đoán (Inference)", "17/12/2026", "17/12/2026", "19-sagemaker-immersion-day"),
            ("5", "Dọn dẹp tài nguyên để tránh phát sinh chi phí và tổng kết báo cáo thực tập", "18/12/2026", "18/12/2026", "FCAJ Portfolio")
        ],
        "tasks_en": [
            ("Mon", "Explore Amazon SageMaker Studio and prepare data with Data Wrangler", "12/15/2026", "12/15/2026", "19-sagemaker-immersion-day"),
            ("Tue", "Train and auto-tune XGBoost predictive model over analytics dataset", "12/16/2026", "12/16/2026", "19-sagemaker-immersion-day"),
            ("Wed", "Deploy Serverless Inference Endpoint and test predictive inference", "12/17/2026", "12/17/2026", "19-sagemaker-immersion-day"),
            ("Thu", "Execute resource cleanup and finalize comprehensive internship documentation", "12/18/2026", "12/18/2026", "FCAJ Portfolio")
        ]
    }
]

for w in weeks_data:
    folder_name = f"1.{w['num']}-Week{w['num']}"
    target_dir = os.path.join(content_dir, folder_name)
    os.makedirs(target_dir, exist_ok=True)
    
    # Vietnamese file
    vi_path = os.path.join(target_dir, "_index.vi.md")
    vi_tasks = "\n".join([f"| **{t[0]}** | {t[1]} | {t[2]} | {t[3]} | `{t[4]}` |" for t in w["tasks_vi"]])
    vi_content = f"""---
title: "{w['title_vi']}"
date: {w['date']}
weight: {w['weight']}
chapter: false
pre: " <b> 1.{w['num']}. </b> "
draft: true
---

### Mục tiêu tuần {w['num']}:
* {w['obj_vi'][0]}
* {w['obj_vi'][1]}

---

### Các công việc dự kiến triển khai:
| Thứ | Nội dung công việc | Bắt đầu | Hoàn thành | Nguồn tài liệu |
| :---: | :--- | :---: | :---: | :--- |
{vi_tasks}

---

### Kết quả & Bằng chứng thực tế (Sẽ cập nhật khi hoàn thành):
*(Nội dung đang được triển khai theo tiến độ thực tập. Khi có sản phẩm và bằng chứng thực tế sẽ được cập nhật và gỡ bỏ nhãn draft).*
"""
    with open(vi_path, "w", encoding="utf-8") as f:
        f.write(vi_content)
        
    # English file
    en_path = os.path.join(target_dir, "_index.md")
    en_tasks = "\n".join([f"| **{t[0]}** | {t[1]} | {t[2]} | {t[3]} | `{t[4]}` |" for t in w["tasks_en"]])
    en_content = f"""---
title: "{w['title_en']}"
date: {w['date']}
weight: {w['weight']}
chapter: false
pre: " <b> 1.{w['num']}. </b> "
draft: true
---

### Week {w['num']} Objectives:
* {w['obj_en'][0]}
* {w['obj_en'][1]}

---

### Planned Tasks:
| Day | Task Description | Start Date | Completion Date | Reference Material |
| :---: | :--- | :---: | :---: | :--- |
{en_tasks}

---

### Results & Deliverables (In Progress):
*(Content is being tracked along the internship roadmap. Will be updated with real production evidence and undrafted upon delivery).*
"""
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_content)

print("Successfully updated all Worklog weeks 3 to 12 with realistic Data & Analytics roadmap while keeping draft: true!")
