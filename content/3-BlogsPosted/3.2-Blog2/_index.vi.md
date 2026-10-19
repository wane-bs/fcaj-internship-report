---
title: "Blog 2"
date: 2026-10-19
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
draft: true
---

# TỐI ƯU HÓA CHI PHÍ VÀ BẢO MẬT TRUY CẬP AMAZON S3 VỚI VPC ENDPOINTS

Khi các hệ thống xử lý dữ liệu (Data Lake, Analytics Pipeline) mở rộng trên AWS, lượng dữ liệu trung chuyển giữa máy chủ ảo (EC2, ECS, EKS) và lưu trữ đối tượng Amazon S3 tăng lên nhanh chóng. Việc đi qua cổng Internet Gateway (NAT Gateway) không chỉ tiềm ẩn rủi ro lộ lọt dữ liệu mà còn phát sinh chi phí truyền tải (Data Processing Fee) đáng kể. Giải pháp kiến trúc chuẩn mực được AWS khuyến nghị là sử dụng **Amazon VPC Endpoints**.

### 1. Phân biệt Gateway Endpoint và Interface Endpoint cho S3

| Tiêu chí | Gateway Endpoint (S3) | Interface Endpoint (S3 - AWS PrivateLink) |
| :--- | :--- | :--- |
| **Chi phí** | **Hoàn toàn miễn phí** (0$/giờ, 0$ Data Processing) | Tính phí theo giờ sử dụng và lượng dữ liệu xử lý |
| **Cơ chế định tuyến** | Cập nhật Route Table trong VPC hướng về S3 Prefix List | Sử dụng Elastic Network Interface (ENI) với Private IP |
| **Phạm vi truy cập** | Chỉ trong phạm vi VPC cục bộ | Hỗ trợ truy cập từ On-Premises (Direct Connect / VPN) |
| **Bảo mật** | Gắn Endpoint Policy trực tiếp | Security Group + Endpoint Policy |

### 2. Best Practices triển khai
- **Nguyên tắc phân tầng**: Sử dụng Gateway Endpoint cho toàn bộ tài nguyên nội bộ VPC để loại bỏ hoàn toàn chi phí NAT Gateway.
- **Mở rộng kết nối lai (Hybrid)**: Kết hợp Interface Endpoint để các trung tâm dữ liệu tại chỗ (On-Premises) đẩy trực tiếp dữ liệu vào S3 qua đường truyền riêng.
- **Endpoint Policy**: Luôn thiết lập chính sách truy cập tối thiểu, chỉ cho phép kết nối đến đúng các S3 Buckets nội bộ của tổ chức.

*(Khung bài viết chuẩn bị đăng trên cộng đồng AWS Study Group)*