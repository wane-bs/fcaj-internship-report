---
title: "Worklog Tuần 4"
date: 2026-10-21
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
draft: false
---

### Mục tiêu tuần 4:

* Thiết kế và triển khai kiến trúc mạng ảo tùy biến **Amazon Virtual Private Cloud (Custom VPC)** đa vùng sẵn sàng (Multi-AZ) theo chuẩn AWS Well-Architected.
* Phân hoạch dải địa chỉ IP (CIDR Blocks) cho hệ thống mạng phân tầng gồm 2 Public Subnets và 2 Private Subnets.
* Cấu hình Internet Gateway (`ASG-IGW`) và bảng định tuyến Public Route Table hỗ trợ cấp phát Public IPv4 tự động.
* Thiết lập kiến trúc định tuyến an toàn cho Private Subnets và tích hợp lá chắn kiểm soát chi phí (FinOps Guardrails) cho các dịch vụ mạng nâng cao (NAT Gateway, Site-to-Site VPN).

---

### Các công việc triển khai trong tuần:

| Thứ | Nội dung công việc | Trạng thái | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- |
| **2** | - Phân hoạch dải địa chỉ CIDR `10.10.0.0/16` cho Custom VPC `ASG`.<br>- Tự động hóa khởi tạo VPC và 4 Subnets Multi-AZ qua CloudFormation template `iac/week4-vpc-core.yaml`. | Hoàn thành | VPC ID: `vpc-0192f88a9d299fc9b`. |
| **3** | - Tạo Internet Gateway `ASG-IGW` và đính kèm (attach) vào VPC.<br>- Cấu hình `ASG-Public-RT` với tuyến đường mặc định `0.0.0.0/0` trỏ về Internet Gateway.<br>- Bật cờ `MapPublicIpOnLaunch` cho cả 2 Public Subnets. | Hoàn thành | `igw-040b1ff36a17f6e15` (Active). |
| **4** | - Cấu hình bảng định tuyến `ASG-Private-RT` cô lập hoàn toàn cho Private Subnets.<br>- Xây dựng kịch bản kiểm soát chi phí FinOps: Chỉ bật NAT Gateway thử nghiệm ngắn hạn và dọn dẹp tức thì qua script tự động. | Hoàn thành | Script `scripts/cleanup_week4_vpc.ps1`. |
| **5** | - Nghiên cứu tài liệu kỹ thuật kết nối mạng lai Site-to-Site VPN với Libreswan trên Amazon Linux 2023 (`03-vpc-site-to-site-vpn`).<br>- Thiết lập kiến trúc quản trị máy chủ qua AWS Systems Manager (SSM Session Manager) không cần mở cổng SSH 22. | Hoàn thành | Zero open ports, an toàn bảo mật. |

---

### Chi tiết các bước triển khai & Bằng chứng thực tế:

#### 1. Quy hoạch dải địa chỉ mạng (CIDR Subnetting Plan)
Hệ thống mạng được phân chia khoa học trên dải mạng lớn `10.10.0.0/16`, trải dài trên 2 Availability Zones (`us-east-1a` và `us-east-1b`):

| Subnet Tên | Availability Zone | CIDR Block | Loại Subnet | Tự động cấp Public IP |
| :--- | :---: | :---: | :---: | :---: |
| `ASG-Public-Subnet-1` | `us-east-1a` | `10.10.1.0/24` | Public | **True** |
| `ASG-Public-Subnet-2` | `us-east-1b` | `10.10.2.0/24` | Public | **True** |
| `ASG-Private-Subnet-1` | `us-east-1a` | `10.10.3.0/24` | Private | **False** |
| `ASG-Private-Subnet-2` | `us-east-1b` | `10.10.4.0/24` | Private | **False** |

---

#### 2. Tự động hóa triển khai hạ tầng mạng qua CloudFormation
Toàn bộ kiến trúc mạng lõi được đóng gói trong tệp `iac/week4-vpc-core.yaml` (100% miễn phí, không phát sinh chi phí duy trì):

```powershell
aws cloudformation deploy `
    --template-file iac/week4-vpc-core.yaml `
    --stack-name fcaj-week4-vpc `
    --profile fcaj-admin
```
Kết quả thực thi thành công: `Successfully created/updated stack - fcaj-week4-vpc`.

![Khởi tạo Custom VPC ASG trên AWS Console](/images/1-Worklog/1.4-Week4/01_create_custom_vpc.png)

![Phân hoạch 4 Subnets Multi-AZ](/images/1-Worklog/1.4-Week4/02_subnets_multi_az.png)

---

#### 3. Nghiệm thu thực tế trên AWS CLI

##### A. Kiểm tra trạng thái VPC `ASG`
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

##### B. Kiểm tra danh sách 4 Subnets Multi-AZ
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

##### C. Kiểm tra Internet Gateway và Bảng định tuyến
```powershell
# Kiểm tra Internet Gateway
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

![Đính kèm Internet Gateway vào VPC ASG](/images/1-Worklog/1.4-Week4/03_attach_internet_gateway.png)

![Cấu hình bảng định tuyến Public Route Table](/images/1-Worklog/1.4-Week4/04_route_table_default_route.png)

Bảng định tuyến `ASG-Public-RT` (`rtb-05bf77bf94acbf8b0`) đã kích hoạt tuyến đường `0.0.0.0/0` trỏ thẳng ra `igw-040b1ff36a17f6e15`, cho phép các máy chủ trong Public Subnet kết nối Internet hai chiều. Trong khi đó, `ASG-Private-RT` (`rtb-0a0c944c4d90bfa3d`) hoàn toàn cô lập các Private Subnet, không có tuyến đường ra Internet.

---

#### 4. Chốt chặn FinOps: Kiểm soát chi phí dịch vụ mạng
Các dịch vụ như **NAT Gateway** (\$0.045/giờ) và **Site-to-Site VPN Connection** (\$0.05/giờ) nếu bật liên tục sẽ làm cạn kiệt nguồn tài trợ \$100 Credit. Do đó, hệ thống áp dụng cơ chế:
- **Kiểm toán Zero-Waste**: Kiểm tra định kỳ để đảm bảo không có tài nguyên phát sinh chi phí nào bị bỏ quên.
```powershell
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=vpc-0192f88a9d299fc9b" --profile fcaj-admin
aws ec2 describe-vpn-connections --profile fcaj-admin
```
Kết quả ghi nhận: `NatGateways: []` và `VpnConnections: []` (Hoàn toàn an toàn).

![Kiến trúc định tuyến qua NAT Gateway](/images/1-Worklog/1.4-Week4/05_nat_gateway_architecture.png)

![Quản trị an toàn qua AWS Systems Manager Session Manager](/images/1-Worklog/1.4-Week4/06_ssm_session_manager.png)

- **Kịch bản dọn dẹp tự động**: Khi cần thử nghiệm hoặc bàn giao bài lab, chạy script dọn dẹp tức thời `.\scripts\cleanup_week4_vpc.ps1` để tự động thu hồi tài nguyên CloudFormation.

---

### Kết quả đạt được trong tuần 4:

* **Hạ tầng mạng chuẩn Enterprise**: Khởi tạo thành công VPC đa vùng sẵn sàng `ASG` với kiến trúc 4 Subnets phân tách ranh giới an ninh rõ ràng.
* **Tự động hóa 100% qua IaC**: Mọi tài nguyên VPC, Subnets, Gateway và Route Tables đều được quản lý bằng CloudFormation template chuẩn mực, dễ dàng tái tạo.
* **Bảo vệ tài chính chủ động (FinOps Guardrails)**: Đảm bảo toàn bộ kiến trúc lõi hoạt động với chi phí \$0.00, sẵn sàng cho các bài thực hành nâng cao ở các tuần tiếp theo (EC2, RDS PostgreSQL, S3 VPC Endpoints).
* **Minh chứng trực quan đầy đủ**: Tích hợp 6 hình ảnh sơ đồ và giao diện AWS Console thực tế minh họa trực quan mọi bước thực thi.
