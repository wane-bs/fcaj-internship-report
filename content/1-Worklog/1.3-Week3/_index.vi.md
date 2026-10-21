---
title: "Worklog Tuần 3"
date: 2026-10-14
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
draft: false
---

### Mục tiêu tuần 3:

* Nắm vững kiến trúc quản trị danh tính và kiểm soát truy cập (IAM Governance) theo nguyên tắc Đặc quyền tối thiểu (Least Privilege).
* Tự động hóa triển khai nhóm quản trị (`AdminGroup`), vai trò ủy quyền (`AdminRole`), và tài khoản vận hành (`OperatorUser`) qua AWS CloudFormation.
* Thiết lập cơ chế nâng quyền tạm thời (Role Switching) thông qua AWS Security Token Service (STS) thay vì gán quyền quản trị cố định.
* Xác minh tính toàn vẹn của hệ sinh thái kiểm toán an ninh thông qua AWS CloudTrail.

---

### Các công việc đã triển khai trong tuần:

| Thứ | Nội dung công việc | Trạng thái | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- |
| **2** | - Nghiên cứu kiến trúc phân quyền IAM và nguyên tắc Least Privilege.<br>- Xây dựng cấu trúc CloudFormation template cho toàn bộ tài nguyên IAM Tuần 3. | Hoàn thành | Tệp `iac/week3-iam.yaml`. |
| **3** | - Triển khai Stack `fcaj-week3-iam` qua AWS CLI.<br>- Khởi tạo `AdminGroup` gán chính sách `AdministratorAccess`.<br>- Khởi tạo `AdminRole` thiết lập quan hệ tin cậy (Trust Relationship) với Account ID cá nhân. | Hoàn thành | `StackStatus: CREATE_COMPLETE`. |
| **4** | - Khởi tạo `OperatorUser` với quyền Console nhưng không cấp bất kỳ Group hay Managed Policy nào.<br>- Gán Inline Policy `AllowOperatorAssumeAdminRole` chỉ cho phép gọi hành động `sts:AssumeRole` tới đúng ARN của `AdminRole`. | Hoàn thành | Kiểm toán: `Groups: []` (Least Privilege). |
| **5** | - Viết script `scripts/test_assume_role.ps1` kiểm thử nâng quyền tự động qua dòng lệnh CLI.<br>- Thực hiện Switch Role trên AWS Console để kiểm thử trải nghiệm quản trị tạm thời.<br>- Tra cứu và đối soát sự kiện `AssumeRole` ghi nhận trên AWS CloudTrail. | Hoàn thành | CloudTrail Event: `AssumeRole` thành công. |

---

### Chi tiết các bước triển khai & Bằng chứng thực tế:

#### 1. Tự động hóa khởi tạo tài nguyên IAM qua AWS CloudFormation
Nhằm đảm bảo tính nhất quán và khả năng tái lập (Infrastructure as Code - IaC), toàn bộ các thực thể IAM được định nghĩa trong mẫu template `iac/week3-iam.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'FCAJ Week 3: IAM Least Privilege and STS Role Switching Lab'

Parameters:
  OperatorPassword:
    Type: String
    NoEcho: true
    MinLength: 8
    Description: 'Initial password for OperatorUser (passed securely at deploy time)'


Resources:
  AdminGroup:
    Type: AWS::IAM::Group
    Properties:
      GroupName: AdminGroup
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess

  AdminRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: AdminRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess

  OperatorUser:
    Type: AWS::IAM::User
    Properties:
      UserName: OperatorUser
      LoginProfile:
        Password: !Ref OperatorPassword
        PasswordResetRequired: false

  OperatorAssumeAdminPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: AllowOperatorAssumeAdminRole
      Users:
        - !Ref OperatorUser
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: ExplicitAssumeAdminRole
            Effect: Allow
            Action: 'sts:AssumeRole'
            Resource: !GetAtt AdminRole.Arn
```

Thực thi triển khai thông qua AWS CLI:
```powershell
aws cloudformation deploy `
    --template-file iac/week3-iam.yaml `
    --stack-name fcaj-week3-iam `
    --capabilities CAPABILITY_NAMED_IAM `
    --profile fcaj-admin
```
Kết quả ghi nhận trạng thái: `Successfully created/updated stack - fcaj-week3-iam`.

![Khởi tạo Admin Group trên IAM Console](/images/1-Worklog/1.3-Week3/01_create_admin_group.png)

![Thiết lập quan hệ tin cậy cho Admin Role](/images/1-Worklog/1.3-Week3/02_create_admin_role_trust.png)

---

#### 2. Kiểm toán bảo mật danh tính theo nguyên tắc Least Privilege
Sau khi Stack khởi tạo xong, hệ thống tiến hành kiểm tra tính cô lập của người dùng `OperatorUser`:

```powershell
# Kiểm tra các Group được gán cho OperatorUser
aws iam list-groups-for-user --user-name OperatorUser --profile fcaj-admin

# Kiểm tra Inline Policy gán cho OperatorUser
aws iam list-user-policies --user-name OperatorUser --profile fcaj-admin
```

Kết quả phản hồi từ AWS IAM:
```json
{
    "Groups": []
}
{
    "PolicyNames": [
        "AllowOperatorAssumeAdminRole"
    ]
}
```

![Khởi tạo người dùng OperatorUser](/images/1-Worklog/1.3-Week3/03_create_operator_user.png)

![Cấu hình Inline Policy sts:AssumeRole cho OperatorUser](/images/1-Worklog/1.3-Week3/04_inline_policy_assume_role.png)

> [!NOTE]
> Kết quả `Groups: []` chứng minh `OperatorUser` tuân thủ nghiêm ngặt nguyên tắc **Zero Default Privileges**. Người dùng này không thể tự ý xem hay chỉnh sửa bất kỳ tài nguyên điện toán/lưu trữ nào nếu chưa thực hiện phiên nâng quyền.

---

#### 3. Kiểm thử cơ chế nâng quyền tạm thời qua AWS STS AssumeRole
Để cấp quyền hạn đặc biệt một cách an toàn mà không cần cấp quyền vĩnh viễn, người dùng thực thi lời gọi `sts:AssumeRole`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test_assume_role.ps1
```

Nhật ký thực thi trả về từ AWS Security Token Service:
```text
=== Bat dau kiem thu STS AssumeRole cho Tuan 3 ===
Account ID: 658302145298
Target Role ARN: arn:aws:iam::658302145298:role/AdminRole
Dang goi lenh STS AssumeRole qua profile fcaj-admin...

=== STS AssumeRole THANH CONG! ===
Assumed Role User ARN : arn:aws:sts::658302145298:assumed-role/AdminRole/FCAJ-OperatorSession
Temporary AccessKeyId : ASIA**************** (REDACTED)
Expiration Time       : 2026-10-21T04:53:49+00:00

Da san sang phan quyen tam thoi cho OperatorUser!
```
Hệ thống STS đã cấp phát thành công cặp khóa tạm thời (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) có thời hạn sống hữu hạn (15 phút), giảm thiểu triệt để rủi ro rò rỉ khóa dài hạn.

---

#### 4. Quy trình chuyển đổi vai trò (Switch Role) trên AWS Console
Người dùng có thể trải nghiệm tính năng này trực tiếp trên trình duyệt:
1. Đăng nhập AWS Management Console bằng tài khoản `OperatorUser` và mật khẩu đã khởi tạo bảo mật (`[YOUR_SECURE_PASSWORD]`).
2. Bấm vào tên người dùng ở góc trên bên phải $\rightarrow$ Chọn **Switch Role**.
3. Điền thông tin:
   - **Account ID**: `658302145298`
   - **Role**: `AdminRole`
   - **Display Name**: `Admin-Access`

![Cấu hình chuyển đổi vai trò Switch Role trên giao diện Console](/images/1-Worklog/1.3-Week3/05_switch_role_configuration.png)

4. Xác nhận chuyển đổi: Thanh điều hướng AWS Console đổi sang màu sắc vai trò mới, xác nhận phiên làm việc đã được cấp quyền `AdministratorAccess` tạm thời.

![Giao diện Console đổi sang màu sắc vai trò quản trị AdminRole](/images/1-Worklog/1.3-Week3/06_switch_role_success_banner.png)

5. Sau khi hoàn thành tác vụ quản trị, bấm **Switch back** để hoàn về quyền hạn cơ bản an toàn.

---

#### 5. Kiểm tra dấu vết kiểm toán trên AWS CloudTrail
Toàn bộ hành vi gọi hàm `AssumeRole` đều được AWS CloudTrail lưu trữ phục vụ điều tra sự cố:
```powershell
aws cloudtrail lookup-events `
    --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole `
    --max-results 1 `
    --query "Events[0].[EventName,Username,EventTime]" `
    --output table `
    --profile fcaj-admin
```
```text
-------------------------------
|        LookupEvents         |
+-----------------------------+
|  AssumeRole                 |
|  hieu-admin                 |
|  2026-10-21T11:02:08+07:00  |
+-----------------------------+
```

---

### Kết quả đạt được trong tuần 3:

* **Mô hình bảo mật chuẩn Enterprise**: Xây dựng thành công kiến trúc phân quyền dựa trên vai trò (Role-Based Access Control - RBAC) kết hợp ủy quyền tạm thời (STS).
* **Tuân thủ Least Privilege**: Loại bỏ hoàn toàn thói quen gán quyền Administrator cố định cho người dùng; mọi tác vụ rủi ro cao đều phải thông qua phiên AssumeRole có ghi vết.
* **Tự động hóa hoàn toàn qua IaC**: Toàn bộ hệ thống IAM được quản lý bằng CloudFormation, cho phép triển khai hoặc dọn dẹp môi trường chỉ với một câu lệnh CLI duy nhất.
* **Minh chứng trực quan đầy đủ**: Tích hợp toàn diện 6 hình ảnh màn hình Console thực tế cùng nhật ký CloudTrail chi tiết.
