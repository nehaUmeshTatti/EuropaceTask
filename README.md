# Infrastructure as Code (IaC) for running a WebService on an EC2 Instance

This repository contains **Infrastructure as Code (IaC)** to deploy the necessary resources to host a web service on an EC2 instance within an AWS account using the AWS Cloud Development Kit (CDK) with Python.

---

## **Prerequisites**

Before proceeding, make sure the following tools are installed and configured:

1. **AWS Account**: An AWS account with sufficient permissions is required to create resources.
2. **AWS CLI**:
   - Install and configure with credentials in the desired region.
   - [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
3. **Python**:
   - Python 3.8 or later required.
   - [Install Python](https://www.python.org/downloads/)
4. **AWS CDK (Python)**:
   - Install the AWS CDK Python libraries:
     ```bash
     pip install aws-cdk.core
     ```
   - Ensure `cdk` command is available:
     ```bash
     cdk --version
     ```

---

## **AWS Resources**

The CDK script provisions the following AWS resources:

- **VPC**:
  - A Virtual Private Cloud (VPC) with private subnet for security.
- **Security Group**:
  - **Inbound rules** for SSH (**port 22**) and HTTPS (**port 443**).
  - **Outbound rules** for HTTPS (**port 443**).
- **IAM Role**:
  - EC2 role with the **AmazonSSMManagedInstanceCore** and **AmazonSSMPatchAssociation** policies, enabling EC2 instance management and additional permissions for interacting with AWS services (e.g., Systems Manager).
- **EC2 Instance**:
  - Amazon EC2 instance running **Amazon Linux 2 AMI**.
  - Includes **Security groups**, **Key pair**, and **User data** for bootstrapping and configuration.
- **S3 Bucket**:
  - S3 Bucket is created and IAM role created is granted read and write permission to access this S3 bucket.
  - Includes **versioning**, **Encryption**, and **removal policy** for bootstrapping and configuration.

## **Steps to Deploy**

### 1. **Clone the Repository**
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd <repository-name>
```
### 2. **Install Dependencies**
Install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```
### 3. **Bootstrap the CDK Environment**
AWS CDK requires bootstrapping for the account/region before deploying resources. Run:
```bash
cdk bootstrap aws://<account-id>/<region>
```
Replace `<account-id>` with your AWS account ID and `<region>` with the desired AWS region (e.g., us-east-1).

### 4. **Run cdk commands**
- Run the following commands to synthesize, deploy or delete the stack
```bash
cdk synth
cdk deploy
cdk destroy
```
### 4. **Run Unit Tests**
- Run the following command to run the unit tests
```bash
pip install -r requirements-dev.txt
pytest
```

