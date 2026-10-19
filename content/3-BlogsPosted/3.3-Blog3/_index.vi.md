---
title: "Blog 3"
date: 2026-10-19
weight: 3
chapter: false
pre: " <b> 3.3. </b> "
draft: true
---

# XÂY DỰNG SERVERLESS DATA LAKE VỚI AWS GLUE, ATHENA VÀ PARQUET

Trong kỷ nguyên dữ liệu lớn (Big Data), việc vận hành các cụm máy chủ phân tích truyền thống (Hadoop, Spark cluster) đòi hỏi chi phí bảo trì và nhân lực rất lớn. Mô hình **Serverless Data Lake** trên AWS giúp các kỹ sư dữ liệu loại bỏ hoàn toàn gánh nặng quản lý máy chủ mà vẫn đảm bảo hiệu năng truy vấn hàng terabyte dữ liệu trong vài giây.

### 1. Kiến trúc 3 tầng chuẩn mực (Modern Data Architecture)
- **Tầng Lưu trữ (S3 Storage Tier)**: Phân tách rõ ràng giữa *Raw Zone* (dữ liệu thô JSON/CSV), *Clean Zone* (dữ liệu đã lọc sạch), và *Curated Zone* (dữ liệu định dạng Parquet nén Snappy).
- **Tầng Khám phá & Metadata (AWS Glue Data Catalog)**: Tự động trích xuất schema qua Glue Crawlers, hỗ trợ đồng bộ schema evolution khi cấu trúc dữ liệu nguồn thay đổi.
- **Tầng Truy vấn Serverless (Amazon Athena)**: Thực thi truy vấn SQL ANSI trực tiếp trên S3 mà không cần nạp vào cơ sở dữ liệu vật lý.

### 2. Các đòn bẩy FinOps tối ưu chi phí
- **Chuyển đổi sang Parquet**: Tiết kiệm 80-90% dung lượng lưu trữ so với text/CSV.
- **Partitioning theo thời gian**: Giảm 95% lượng dữ liệu quét (Scanned Bytes) trên Athena, cắt giảm trực tiếp chi phí truy vấn ($5 / TB scan).
- **Tích hợp QuickSight**: Kết nối trực tiếp Athena làm Data Source để trực quan hóa báo cáo BI tức thì.

*(Khung bài viết chuẩn bị đăng trên cộng đồng AWS Study Group)*