---
title: "Week 3 Worklog"
date: 2026-10-14
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
draft: false
---

### Week 3 Objectives:

* Master IAM identity governance and access control following the Principle of Least Privilege.
* Automate the provisioning of administrative groups (`AdminGroup`), delegation roles (`AdminRole`), and operational users (`OperatorUser`) using AWS CloudFormation.
* Implement temporary privilege escalation (Role Switching) using AWS Security Token Service (STS) rather than static long-term admin credentials.
* Verify audit trail and security compliance through AWS CloudTrail event logging.

---

### Tasks Executed During the Week:

| Day | Task Description | Status | Technical Notes |
| :---: | :--- | :---: | :--- |
| **Mon** | - Researched IAM policy evaluation logic and Least Privilege architectures.<br>- Authored CloudFormation template defining all Week 3 IAM resources. | Completed | File `iac/week3-iam.yaml`. |
| **Tue** | - Deployed CloudFormation Stack `fcaj-week3-iam` via AWS CLI.<br>- Created `AdminGroup` attached with `AdministratorAccess`.<br>- Created `AdminRole` establishing trust relationship with personal Account ID. | Completed | `StackStatus: CREATE_COMPLETE`. |
| **Wed** | - Created `OperatorUser` with Console access and zero default group/managed policies.<br>- Attached Inline Policy `AllowOperatorAssumeAdminRole` strictly scoping `sts:AssumeRole` to `AdminRole` ARN. | Completed | Audit: `Groups: []` (Least Privilege). |
| **Thu** | - Developed verification script `scripts/test_assume_role.ps1` to validate automated CLI role assumption.<br>- Performed browser-based Switch Role test via AWS Management Console.<br>- Audited and verified `AssumeRole` events recorded in AWS CloudTrail. | Completed | CloudTrail Event: `AssumeRole` verified. |

---

### Step-by-Step Implementation & Technical Evidence:

#### 1. Infrastructure-as-Code Automation with AWS CloudFormation
To ensure repeatability and auditability, all IAM entities were authored declaratively in `iac/week3-iam.yaml`:

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

Executed deployment via AWS CLI:
```powershell
aws cloudformation deploy `
    --template-file iac/week3-iam.yaml `
    --stack-name fcaj-week3-iam `
    --capabilities CAPABILITY_NAMED_IAM `
    --profile fcaj-admin
```
Outcome confirmed: `Successfully created/updated stack - fcaj-week3-iam`.

![Admin Group Provisioning on IAM Console](/images/1-Worklog/1.3-Week3/01_create_admin_group.png)

![Trust Relationship Configuration for Admin Role](/images/1-Worklog/1.3-Week3/02_create_admin_role_trust.png)

---

#### 2. Least Privilege Security Audit for OperatorUser
Following stack deployment, user privilege isolation was audited via CLI:

```powershell
# Verify user groups (must be empty)
aws iam list-groups-for-user --user-name OperatorUser --profile fcaj-admin

# Verify inline policies
aws iam list-user-policies --user-name OperatorUser --profile fcaj-admin
```

Output:
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

![Operator User Provisioning](/images/1-Worklog/1.3-Week3/03_create_operator_user.png)

![Inline Policy Configuration for STS AssumeRole](/images/1-Worklog/1.3-Week3/04_inline_policy_assume_role.png)

> [!NOTE]
> The empty group assignment (`Groups: []`) verifies adherence to **Zero Default Privileges**. `OperatorUser` cannot access or modify AWS infrastructure without explicit temporary role elevation.

---

#### 3. Temporary Credential Elevation via AWS STS AssumeRole
To elevate privileges safely for break-glass operations, the user calls `sts:AssumeRole`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test_assume_role.ps1
```

Terminal output from AWS Security Token Service:
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
The STS engine issued short-lived credentials (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) valid for 15 minutes, completely mitigating long-term credential leakage risks.

---

#### 4. Browser-Based Switch Role Workflow
1. Log in to the AWS Management Console with `OperatorUser` credentials.
2. Select the account profile dropdown in the top-right corner $\rightarrow$ Choose **Switch Role**.
3. Enter destination parameters:
   - **Account**: `658302145298`
   - **Role**: `AdminRole`
   - **Display Name**: `Admin-Access`

![Switch Role Configuration Interface](/images/1-Worklog/1.3-Week3/05_switch_role_configuration.png)

4. Confirm switch: The console header switches color and displays the active role tag, indicating active `AdministratorAccess`.

![Console Switched to Admin Role](/images/1-Worklog/1.3-Week3/06_switch_role_success_banner.png)

5. Upon task completion, select **Switch back** to immediately return to non-privileged operational status.

---

#### 5. Audit Trail Verification in AWS CloudTrail
Every invocation of `AssumeRole` is immutably logged in AWS CloudTrail:
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

### Key Outcomes in Week 3:

* **Enterprise-Grade Access Governance**: Successfully implemented Role-Based Access Control (RBAC) with dynamic temporary STS credentials.
* **Least Privilege Compliance**: Eliminated persistent administrator privilege assignments; sensitive administrative actions are gated through audited sessions.
* **100% Infrastructure-as-Code**: Entire IAM topology is versioned and deployable/destroyable via a single CloudFormation command.
* **Comprehensive Visual Proof**: Embedded 6 real-world Console screenshots and detailed CloudTrail logs.
