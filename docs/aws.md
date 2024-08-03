# AWS Documentation

## Overview

This document provides a brief overview of how to work with AWS services for your project.

## AWS Services Used

### Amazon EC2

- **Purpose**: Provides scalable virtual servers.
- **Instance Types**: t2.micro, t3.medium, etc.
- **Configuration**: 
  - AMI: Ubuntu 20.04 LTS
  - Instance Type: t3.medium
  - Security Group: Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

### Amazon RDS

- **Purpose**: Managed relational database service.
- **Database Engine**: PostgreSQL
- **Configuration**:
  - Instance Class: db.t3.micro
  - Storage Type: General Purpose (SSD)
  - Backup: Enabled

### Amazon S3

- **Purpose**: Object storage for data backup and archiving.
- **Bucket Name**: my-s3-bucket
- **Configuration**:
  - Versioning: Enabled
  - Lifecycle Policies: Transition to Glacier after 1 year

## Setting Up

### EC2 Setup

1. Go to the EC2 Dashboard.
2. Launch a new instance.
3. Choose the appropriate AMI and instance type.
4. Configure instance details, add storage, and configure security groups.
5. Launch and connect to the instance.

### RDS Setup

1. Go to the RDS Dashboard.
2. Create a new database instance.
3. Choose PostgreSQL as the engine and configure the instance settings.
4. Configure backups and monitoring.
5. Launch and connect to the database.

### S3 Setup

1. Go to the S3 Dashboard.
2. Create a new bucket.
3. Configure bucket settings and permissions.
4. Upload files and configure lifecycle policies.

## IAM Roles and Permissions

Ensure that appropriate IAM roles and policies are set up to provide necessary permissions to your EC2 instances and other AWS services.

## Security Best Practices

- Regularly update your instances and databases.
- Use IAM roles and policies to restrict access.
- Enable encryption for data at rest and in transit.
- Set up CloudWatch monitoring and alerts.

## Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/index.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
