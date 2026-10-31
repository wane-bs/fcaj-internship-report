# MA TRẬN PHÂN BỔ CÔNG VIỆC 12 TUẦN & THEO DÕI BẰNG CHỨNG THỰC TẬP (FCAJ TRACKING MATRIX)
<!-- maintained-by: antigravity-ide | domain: enterprise-financial-data-lakehouse -->

Tài liệu này đóng vai trò kim chỉ nam điều phối, liên kết chặt chẽ từng bài thực hành Worklog hàng tuần với kiến trúc tổng thể của **Đề án Enterprise Financial Data Lakehouse**.

---

## 1. MA TRẬN THEO DÕI TIẾN TRÌNH 12 TUẦN (E2E PROGRESS TRACKER)

| Tuần | Trạng thái | Lĩnh vực AWS | Mục tiêu Kỹ thuật trong Đề án | Bằng chứng Console / IaC Code | Liên kết Worklog |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **W1** | **Hoàn thành** | Account & Billing | Khởi tạo tài khoản AWS, kích hoạt thành công \$100 AWS Credit tài trợ, thiết lập cấu hình quản lý hạn mức ngân sách ban đầu. | `aws_billing_100credit.png` | [Tuần 1](content/1-Worklog/1.1-Week1/) |
| **W2** | **Hoàn thành** | Security & FinOps | Thiết lập Day-0 Security Guardrails: Chuyển đổi định danh sang IAM Identity Center (SSO), cấu hình Zero-Trust MFA và CloudWatch Billing Alarms. | `iam_sso_configured.png`, `cloudwatch_budget_alarm.png` | [Tuần 2](content/1-Worklog/1.2-Week2/) |
| **W3** | **Hoàn thành** | IAM Governance | Chuẩn hóa phân quyền Least Privilege, tự động hóa khởi tạo AdminGroup, OperatorUser và vai trò ủy quyền qua AWS CloudFormation. | `iac/week3-iam-role-switching.yaml`, `switch_role_evidence.png` | [Tuần 3](content/1-Worklog/1.3-Week3/) |
| **W4** | **Hoàn thành** | Networking | Thiết kế và triển khai kiến trúc mạng phân tầng bảo mật Amazon Custom VPC Multi-AZ (2 Public Subnets, 2 Private Subnets, Route Tables). | `iac/week4-vpc-multi-az.yaml`, `vpc_subnets_routing.png` | [Tuần 4](content/1-Worklog/1.4-Week4/) |
| **W5** | **Hoàn thành** | Compute & Storage | Triển khai **Data Ingestion Worker** (EC2 Linux) trong Private Subnet; Tự động hóa qua User Data; Cấu hình mount thêm EBS Volume 20GB lưu cache staging; Xử lý sự cố mất Key Pair. | `iac/week5-ec2-ingestion-worker.yaml`, `scripts/week5_mount_ebs.sh`, `lsblk` / `df -h` logs | [Tuần 5](content/1-Worklog/1.5-Week5/) |
| **W6** | **Hoàn thành** | Database & Secrets | Khởi tạo **Master Metadata Relational Store** (Amazon RDS PostgreSQL) lưu trữ `Dim_Asset` & `Dim_Date`; Bảo mật kết nối tuyệt đối bằng AWS Secrets Manager. | `iac/week6-rds-metadata-store.yaml`, `scripts/week6_test_db_connection.py`, Secrets Manager logs | [Tuần 6](content/1-Worklog/1.6-Week6/) |
| **W7** | *Kế hoạch* | S3 & PrivateLink | Xây dựng **Medallion Data Lakehouse** (Bronze/Silver/Gold buckets); Cấu hình S3 Gateway VPC Endpoint loại bỏ phí NAT Gateway và thiết lập S3 Bucket Policy siết chặt truy cập. | S3 Lakehouse Buckets, VPC Endpoint route table, CLI upload test via Endpoint | [Tuần 7](content/1-Worklog/1.7-Week7/) |
| **W8** | *Kế hoạch* | Glue & Metadata | Thiết lập **AWS Glue Data Catalog**; Chạy Glue Crawler tự động suy luận schema; Xây dựng Glue ETL PySpark Job làm sạch và chuyển đổi sang Parquet Snappy phân vùng theo `year/ticker`. | Glue Data Catalog Tables, Glue ETL Job diagram, CloudWatch Glue Execution logs | [Tuần 8](content/1-Worklog/1.8-Week8/) |
| **W9** | *Kế hoạch* | Athena Serverless SQL | Tối ưu hóa truy vấn phân tích định lượng tài chính bằng **Amazon Athena**; Áp dụng CTAS, Columnar Parquet và Partition Projection giảm >85% dung lượng quét và chi phí truy vấn. | Athena Query Editor logs, Execution Time & Data Scanned metrics, CTAS table results | [Tuần 9](content/1-Worklog/1.9-Week9/) |
| **W10** | *Kế hoạch* | NoSQL Feature Store | Xây dựng **Real-Time Financial Feature Store** trên Amazon DynamoDB (Single-Table Design); Tích hợp Python Boto3 SDK nạp và truy vấn 18 biến $t-1$ với độ trễ < 10ms. | DynamoDB Table Items, Boto3 script CRUD operations, GSI query benchmark logs | [Tuần 10](content/1-Worklog/1.10-Week10/) |
| **W11** | *Kế hoạch* | BI & Visualization | Kết nối Amazon QuickSight vào Athena Data Lake; Thiết kế **Executive Financial Risk Dashboard** trực quan hóa biến động thị trường, danh mục ngân hàng và cảnh báo Basel Zones. | QuickSight Interactive Dashboard, Visual Sheets (KPIs, Heatmap, Waterfall), Dataset config | [Tuần 11](content/1-Worklog/1.11-Week11/) |
| **W12** | *Kế hoạch* | GenAI & Project Review | Tích hợp Amazon Bedrock / SageMaker tóm tắt tự động rủi ro thị trường hàng ngày; Kiểm toán FinOps toàn diện chu kỳ thực tập; Đóng gói nghiệm thu Đề án tốt nghiệp FCAJ. | Final Cost Audit Report, Clean-up / Termination scripts, Comprehensive Portfolio Showcase | [Tuần 12](content/1-Worklog/1.12-Week12/) |

---

## 2. QUY TRÌNH CHUẨN KHI BÀN GIAO MỖI TUẦN WORKLOG (WORKLOG SENTINEL CHECKLIST)

Mỗi khi hoàn thành một tuần thực hành từ Tuần 5 đến Tuần 12, AI Agent cùng Nguyễn Trung Hiếu bắt buộc thực hiện kiểm tra 4 tiêu chí:
1. **FrontMatter chuẩn**: Đảm bảo `draft: false`, cập nhật đầy đủ tiêu đề và ngày hoàn thành.
2. **Song ngữ đồng bộ**: Hoàn thành đồng thời cả 2 tệp `_index.vi.md` và `_index.md`.
3. **Mã nguồn IaC / Script**: Lưu trữ toàn bộ mã nguồn liên quan vào thư mục `iac/` hoặc `scripts/`.
4. **Bằng chứng thực tế (Console Evidence)**: Đầy đủ ảnh chụp màn hình hoặc log terminal lưu trong `static/images/1-Worklog/1.X-WeekX/`.
