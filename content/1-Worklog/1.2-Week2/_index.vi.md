---
title: "Worklog Tuần 2"
date: 2026-10-07
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
draft: false
---

### Mục tiêu tuần 2:

* Thiết lập an toàn ngay lập tức cho tài khoản AWS mới tạo (Day 0 Security & FinOps Guardrails).
* Triển khai mô hình định danh hiện đại **IAM Identity Center (AWS SSO)** thay thế hoàn toàn cho Access Key cố định nguy hiểm.
* Thiết lập các chốt chặn ngân sách (**AWS Budgets**) và hệ thống giám sát kiểm toán toàn diện (**AWS CloudTrail**).
* Tích hợp môi trường phát triển cục bộ và Antigravity IDE với **AWS CLI v2**, **AWS Agent Toolkit** và **AWS MCP Server**.

---

### Các công việc đã triển khai trong tuần:

| Thứ | Nội dung công việc | Trạng thái | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- |
| **2** | - Khởi tạo tài khoản AWS cá nhân (`658302145298`).<br>- Kích hoạt Multi-Factor Authentication (MFA) bảo vệ tài khoản Root.<br>- Cài đặt AWS CLI v2 trên máy tính Windows. | Hoàn thành | Bật MFA qua Authenticator App. |
| **3** | - Tích hợp bộ công cụ trợ lý AI **AWS Agent Toolkit** và nạp **AWS Skill Pack** (`pack-aws` gồm 24 bộ kỹ năng chuyên sâu).<br>- Tích hợp máy chủ **AWS MCP Server** (`aws-mcp`) chính thức qua chuẩn SigV4 vào Antigravity IDE.<br>- Xử lý chuẩn hóa biến môi trường `PATH` trên Windows cho `aws.exe`. | Hoàn thành | Cấu hình 8 công cụ MCP chuyên dụng và 24 AWS Skills. |
| **4** | - Thiết lập lá chắn tài chính **AWS Budgets** (2 tầng cảnh báo):<br>&emsp;+ Ngân sách Zero-Spend (`$0.01/tháng`) phát hiện tức thì tài nguyên quên tắt.<br>&emsp;+ Ngân sách kiểm soát học tập (`$5.00/tháng`) kèm cảnh báo Forecasted.<br>- Định tuyến thông báo email về `01134wane@gmail.com`. | Hoàn thành | Khởi tạo thành công qua CLI automation. |
| **5** | - Cấu hình hạ tầng ghi nhật ký an ninh **AWS CloudTrail** (Multi-Region):<br>&emsp;+ Tạo S3 Bucket lưu trữ nhật ký kiểm toán với chính sách chặn 100% Public Access.<br>&emsp;+ Bật tính năng kiểm tra tính toàn vẹn file log (Log File Validation). | Hoàn thành | `fcaj-management-events-trail` (`IsLogging: True`). |
| **6** | - Khởi tạo **IAM Identity Center (AWS SSO)** tại vùng `us-east-1`.<br>- Tạo User quản trị cá nhân `hieu-admin` và gán Permission Set `AdministratorAccess`.<br>- Cấu hình CLI Profile `fcaj-admin` qua giao diện Web SSO Login.<br>- Khóa và cô lập quyền Root (xóa bỏ toàn bộ Access Key tĩnh). | Hoàn thành | Xác thực danh tính qua Temporary STS Tokens. |

---

### Chi tiết các bước triển khai & Bằng chứng thực tế:

#### 1. Thiết lập Agent Toolkit và AWS MCP Server cho IDE
Nhằm tối ưu hóa năng suất phát triển và tự động hóa các thao tác đám mây trực tiếp từ Antigravity IDE:
- Thực thi lệnh `aws configure agent-toolkit` để tự động dò tìm môi trường phát triển và tải trọn gói 24 bộ kỹ năng chuyên sâu của AWS:

![Cài đặt 24 Skills qua AWS Agent Toolkit](/images/1-Worklog/1.2-Week2/00_agent_toolkit_install.png)

- **AWS Skill Pack (`pack-aws`)**: Tích hợp các bộ kỹ năng chuyên sâu vào `.agents/skills/` bao gồm: Kiến trúc bảo mật (`aws-iam`, `aws-security`, `aws-well-architected-review`), Hạ tầng đám mây (`aws-compute`, `aws-storage`, `aws-networking`, `aws-database`, `aws-serverless`, `aws-containers`), Tự động hóa (`aws-cdk`, `aws-cloudformation`), FinOps (`aws-billing-and-cost-management`) và GenAI (`amazon-bedrock`, `aws-ai-ml`).
- **AWS MCP Server (`aws-mcp`)**: Cấu hình bộ công cụ Model Context Protocol chính thức từ AWS hỗ trợ ký xác thực SigV4, cung cấp 8 công cụ trực tiếp cho AI Agent:
  - `aws___run_script`: Thực thi câu lệnh/script AWS an toàn qua môi trường MCP.
  - `aws___get_presigned_url`: Tải lên/tải xuống S3 hoặc xử lý liên kết file tạm thời an toàn.
  - `aws___search_documentation` & `aws___read_documentation`: Tra cứu trực tiếp tài liệu kỹ thuật và kiến trúc chuẩn từ AWS.
  - `aws___retrieve_skill`: Nạp tự động các hướng dẫn kỹ thuật chuyên sâu từ thư viện AWS.
  - `aws___list_regions` & `aws___get_regional_availability`: Kiểm tra tình trạng khu vực và tính khả dụng của dịch vụ.
  - `aws___get_tasks`: Quản lý tác vụ ngầm kéo dài.
- **Quy tắc định tuyến dự án**: Cấu hình tệp `AGENTS.md` tại thư mục gốc để hướng dẫn AI ưu tiên tương tác qua giao thức MCP thay vì gọi lệnh shell trực tiếp.

#### 2. Thiết lập biến môi trường và Kiểm soát chi phí (AWS Budgets)
Nhằm ngăn chặn việc phát sinh chi phí ngoài tầm kiểm soát và đảm bảo môi trường dòng lệnh CLI hoạt động ổn định trên Windows:
- Chuẩn hóa đường dẫn thực thi AWS CLI trong `User PATH` (`C:\Users\FUJITSU\AppData\Local\Programs\AWSCLIV2\Amazon\AWSCLIV2`).
- Khởi tạo 2 quy tắc ngân sách tự động thông qua `aws budgets create-budget`:
  - `fcaj-zero-spend-alert`: Báo động khi chi phí thực tế > 80% của \$0.01.
  - `fcaj-monthly-5usd-budget`: Báo động khi chi phí đạt \$4.00 hoặc dự báo vượt mốc \$5.00 trong tháng.

#### 3. Kích hoạt IAM Identity Center & Tạo Permission Set
Thay vì tạo IAM User truyền thống với Access Key cố định lưu trên máy (dễ bị lộ khi đẩy code lên Git), mô hình **AWS SSO** đã được áp dụng:
- Bật dịch vụ **IAM Identity Center** trong AWS Organizations.
- Tạo Permission Set chuẩn `AdministratorAccess` cung cấp toàn quyền quản trị hạ tầng một cách an toàn.

![Tạo thành công Permission Set AdministratorAccess](/images/1-Worklog/1.2-Week2/01_permission_set_created.png)

#### 4. Kết nối AWS CLI qua giao diện SSO
Thực hiện liên kết CLI cục bộ với phiên xác thực web thông qua lệnh:
```powershell
aws configure sso
```
Cung cấp SSO start URL (`https://d-90666396a9.awsapps.com/start`) và SSO Region (`us-east-1`):

![Cấu hình SSO Start URL trên Terminal](/images/1-Worklog/1.2-Week2/02_aws_configure_sso_start.png)

#### 5. Gán quyền và Lựa chọn vai trò (Role Assignment)
Hệ thống tự động liên kết User `hieu-admin` với tài khoản AWS `658302145298` và áp dụng vai trò quản trị `AdministratorAccess`. Người dùng lựa chọn profile name mang tên `fcaj-admin`:

![Chọn tài khoản AWS và vai trò quản trị](/images/1-Worklog/1.2-Week2/03_sso_account_role_select.png)

#### 6. Xác thực thành công & Chuyển sang phiên làm việc an toàn
Quá trình đăng nhập và cấp quyền hoàn tất. Trình duyệt xác thực token thành công và trả về thông báo sẵn sàng trên terminal:

![Xác thực CLI Profile thành công](/images/1-Worklog/1.2-Week2/04_sso_login_success.png)

Kiểm tra danh tính hoạt động qua AWS STS:
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

### Kết quả đạt được trong tuần 2:

* **Bảo mật chuẩn Enterprise**: Tài khoản đã được bảo vệ đa lớp (Root MFA, IAM Identity Center SSO, Không có Access Key tĩnh).
* **Lá chắn chi phí chủ động (FinOps Guardrails)**: Đảm bảo kiểm soát chặt chẽ giới hạn Free Tier và phát hiện ngay lập tức bất kỳ dịch vụ tính phí phát sinh.
* **Hệ thống kiểm toán minh bạch**: Toàn bộ hoạt động API trên mọi Region đều được AWS CloudTrail lưu trữ an toàn trong S3 Bucket mã hóa.
* **Tích hợp sâu Agent Toolkit & MCP**: Môi trường phát triển IDE đã được trang bị đầy đủ bộ kỹ năng và MCP Server chính thức của AWS, giúp AI hỗ trợ tra cứu tài liệu, kiến trúc và vận hành đám mây chuẩn xác, an toàn.
