---
title: "Nhật ký công việc"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 1. </b> "
---

# Nhật ký công việc (Worklog)

Chuyên mục **Worklog** ghi lại chi tiết quá trình học tập, thực hành và triển khai các tác vụ công nghệ điện toán đám mây AWS trong suốt thời gian tham gia chương trình thực tập **First Cloud AI Journey (FCAJ)**.

---

### Tiến độ các tuần thực tập

* **[Tuần 1: Khởi tạo tài khoản AWS & Kích hoạt $100 Credit](1.1-week1/)** `[Hoàn thành]`  
  *Kích hoạt tài khoản AWS cá nhân, xác minh $100 AWS Credit tài trợ, tìm hiểu trang quản lý chi phí AWS Billing Console và lập mục tiêu kiểm soát ngân sách.*

* **[Tuần 2: Day 0 Security & FinOps Guardrails](1.2-week2/)** `[Hoàn thành]`  
  *Kích hoạt Root MFA, triển khai IAM Identity Center (AWS SSO), thiết lập lá chắn ngân sách AWS Budgets, kích hoạt AWS CloudTrail và tích hợp AWS MCP Server / Agent Toolkit.*

* **[Tuần 3: Quản trị danh tính IAM & STS Role Switching](1.3-week3/)** `[Hoàn thành]`  
  *Triển khai mô hình phân quyền Least Privilege, tạo AdminGroup, AdminRole và OperatorUser qua CloudFormation, thực thi nâng quyền tạm thời qua AWS STS AssumeRole.*

* **[Tuần 4: Kiến trúc mạng cô lập Custom VPC Multi-AZ](1.4-week4/)** `[Hoàn thành]`  
  *Phân hoạch dải địa chỉ CIDR `10.10.0.0/16`, khởi tạo VPC `ASG` với 4 Subnets Multi-AZ, cấu hình Internet Gateway, Route Tables và lá chắn FinOps Zero-Cost.*

* **[Tuần 5: Quản trị điện toán Amazon EC2 & Lưu trữ EBS](1.5-week5/)** `[Kế hoạch]`  
  *Quản trị máy chủ ảo EC2 Linux, User Data Bootstrap, quản lý khối lưu trữ EBS Volumes và Custom AMI.*

* **[Tuần 6: Cơ sở dữ liệu quan hệ Amazon RDS PostgreSQL](1.6-week6/)** `[Kế hoạch]`  
  *Triển khai RDS PostgreSQL Multi-AZ High Availability, cấu hình Read Replicas và quản lý chứng thực với AWS Secrets Manager.*

* **[Tuần 7: Khởi tạo Data Lake & S3 VPC Endpoints](1.7-week7/)** `[Kế hoạch]`  
  *Xây dựng nền tảng Data Lake trên Amazon S3 phân tầng Raw/Processed/Curated và ứng dụng Gateway VPC Endpoints tối ưu chi phí.*

* **[Tuần 8: Tự động hóa ETL với AWS Glue](1.8-week8/)** `[Kế hoạch]`  
  *Thu thập siêu dữ liệu với Glue Crawlers, quản lý Glue Data Catalog và xây dựng Visual ETL Job chuyển đổi Parquet qua Glue Studio.*

* **[Tuần 9: Phân tích dữ liệu không máy chủ với Amazon Athena](1.9-week9/)** `[Kế hoạch]`  
  *Thực thi truy vấn phân tích Serverless SQL, tối ưu hóa chi phí và tốc độ qua CTAS và kỹ thuật Partitioning.*

* **[Tuần 10: Cơ sở dữ liệu NoSQL tốc độ cao Amazon DynamoDB](1.10-week10/)** `[Kế hoạch]`  
  *Thiết kế Data Model NoSQL, tạo Global Secondary Index (GSI) và tích hợp Python Boto3 SDK.*

* **[Tuần 11: Trực quan hóa dữ liệu kinh doanh với Amazon QuickSight](1.11-week11/)** `[Kế hoạch]`  
  *Kết nối Athena và QuickSight SPICE Engine, thiết kế Interactive BI Dashboards phân tích nghiệp vụ.*

* **[Tuần 12: Ứng dụng Machine Learning với Amazon SageMaker & Tổng kết](1.12-week12/)** `[Kế hoạch]`  
  *Huấn luyện mô hình dự đoán XGBoost trên SageMaker Studio, dọn dẹp tài nguyên và tổng kết toàn diện hồ sơ thực tập FCAJ.*

---

> [!NOTE]
> Tiến độ các bài viết được cập nhật liên tục bám sát tiến độ thực hành và các tiêu chuẩn kiểm toán kiến trúc AWS Well-Architected.