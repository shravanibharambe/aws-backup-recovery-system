# AWS Backup & Recovery System

> An automated AWS backup and recovery system for EC2 data using Amazon EBS Snapshots, AWS Lambda, IAM, and scheduled automation.

---

## 📌 Overview

The **AWS Backup & Recovery System** is a cloud-based backup automation project designed to protect data stored on an Amazon EC2 instance.

The system automatically creates **EBS snapshots** of a designated EBS volume using an AWS Lambda function. A retention policy ensures that only the **3 most recent automated snapshots** are retained, while older snapshots are automatically deleted.

The project also includes recovery testing to verify that backed-up data can be restored successfully.

---

## 🎯 Problem Statement

Data stored on cloud infrastructure can be affected by accidental deletion, system failures, or other operational issues.

Manually creating and managing backups can also become repetitive and difficult to maintain.

This project demonstrates how AWS services can be combined to automate the backup lifecycle and provide a practical recovery mechanism.

---

## 🏗️ Architecture

![AWS Backup & Recovery Architecture](architecture/architecture.png)

### Architecture Flow

```text
                Scheduled Trigger
                       │
                       ▼
                 AWS Lambda
                       │
                       ▼
                Target EBS Volume
                       │
                       ▼
                 EBS Snapshot
                       │
                       ▼
              Retention Management
                       │
              ┌────────┴────────┐
              │                 │
        Latest 3 Kept      Older Deleted
              │
              ▼
          Recovery
              │
              ▼
       Data Validation
```

---

## ☁️ AWS Services Used

| AWS Service            | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| **Amazon EC2**         | Provides the Linux-based compute environment         |
| **Amazon EBS**         | Provides persistent block storage attached to EC2    |
| **EBS Snapshots**      | Creates point-in-time backups of the EBS volume      |
| **AWS Lambda**         | Automates snapshot creation and retention management |
| **Amazon EventBridge** | Triggers the backup process on a schedule            |
| **AWS IAM**            | Controls permissions required by the Lambda function |

---

## ⚙️ How It Works

### 1. Scheduled Backup

A scheduled event triggers the AWS Lambda function automatically.

### 2. Snapshot Creation

Lambda uses the AWS SDK (`boto3`) to create a snapshot of the configured EBS volume.

The target volume is supplied through a Lambda environment variable:

```text
VOLUME_ID
```

This keeps the volume configuration separate from the application logic.

### 3. Snapshot Tagging

Each automated snapshot is tagged with information such as:

```text
Project      = BackupProject
BackupType   = Automated
CreatedAt    = <timestamp>
```

These tags allow the Lambda function to identify snapshots belonging to the project.

### 4. Retention Management

The Lambda function retrieves automated snapshots and sorts them by creation time.

The retention policy keeps the **3 newest snapshots**.

Any snapshots beyond the retention limit are automatically deleted.

```text
Snapshot 1  ← Latest       KEEP
Snapshot 2  ←               KEEP
Snapshot 3  ←               KEEP
Snapshot 4  ← Older         DELETE
Snapshot 5  ← Older         DELETE
```

### 5. Recovery

When recovery is required, an appropriate EBS snapshot can be used to restore the backed-up storage.

The restored data is then validated to confirm that the recovery process was successful.

---

## 🧠 Key Implementation

The backup automation is implemented using Python and `boto3`.

The Lambda function:

* Creates EBS snapshots
* Adds metadata tags
* Retrieves automated project snapshots
* Sorts snapshots by creation time
* Applies the retention policy
* Deletes snapshots beyond the retention limit
* Returns a successful execution response

---

## 🧪 Testing & Validation

The system was tested through the following workflow:

### Backup Test

* Created test data on the EBS volume
* Executed the backup process
* Verified successful snapshot creation

### Retention Test

* Created multiple automated snapshots
* Verified that the newest 3 snapshots were retained
* Verified that older snapshots were removed according to the retention policy

### Recovery Test

* Used the backup snapshot for recovery
* Restored the required storage
* Verified that the test data was successfully recovered

**Result:** Backup, retention, and recovery workflows were successfully validated.

---

## 🔐 Security Considerations

The project follows basic AWS security practices:

* IAM permissions are used to control Lambda access to EC2/EBS resources.
* AWS credentials are not hard-coded into the Lambda function.
* The EBS volume ID is supplied through a Lambda environment variable.
* Private keys and credentials are excluded from the Git repository using `.gitignore`.

---

## 💰 Cost Considerations

AWS resources used in this project can incur charges depending on usage.

Particular attention should be given to:

* EBS snapshot storage
* EBS volumes
* EC2 instance runtime
* Lambda invocations
* Other supporting AWS resources

For a learning project, unnecessary resources should be stopped or deleted when they are no longer required.

---

## 📚 Key Learnings

Through this project, I gained hands-on experience with:

* Amazon EC2 and EBS
* EBS snapshot-based backups
* AWS Lambda automation
* Python with `boto3`
* IAM permissions and execution roles
* Scheduled cloud automation
* Snapshot retention policies
* Cloud recovery workflows
* Backup validation and testing
* Managing AWS resources with automation

---

## 🚀 Future Improvements

Possible improvements to the system include:

* Backup failure notifications using Amazon SNS
* Centralized monitoring using Amazon CloudWatch
* More configurable retention periods
* Backup status reporting
* Cross-region backup replication
* Infrastructure as Code using Terraform or AWS CloudFormation
* Automated recovery testing

---

## 📁 Repository Structure

```text
aws-backup-recovery-system/
│
├── README.md
│
├── architecture/
│   └── architecture.png
│
├── lambda/
│   └── backup_lambda.py
│
└── screenshots/
    ├── 01-infrastructure.png
    ├── 02-backup-snapshot.png
    ├── 03-automation.png
    └── 04-recovery-validation.png
```

---

## ✅ Project Status

**Completed & Tested**

This project was built as a hands-on AWS Cloud project to understand how backup automation, snapshot management, retention policies, and recovery workflows can be implemented using AWS-native services.

---

## 👩‍💻 Author

**Shravani Bharambe**

Cloud & DevOps | AWS | Linux | Networking

[GitHub](https://github.com/shravanibharambe)
