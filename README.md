                                     # backend 

 

 

Django 

 

 

# Env 

 

```python 

python3 -m venv env 

source env/bin/activate 

``` 

 

# Install all libs 

``` 

pip install -r requirements.txt 

``` 

# Run server and create migrates to db 

```python 

python manage.py runserver 

 

python manage.py migrate 

``` 

 

# Create SuperUser 

``` 

python manage.py createsuperuser 

``` 

 

# Sync all libs to file requirements.txt 

 

``` 
pip freeze > requirements.txt

``` 


AWS 

# AWS Documentation 

 

# Overview 

This document provides a brief overview of how to work with AWS services for your project. 

 

# AWS Services Used 

# Amazon EC2 

* Purpose: Provides scalable virtual servers.

* Instance Types: t2.micro, t3.medium, etc.

* Configuration: 

AMI: Ubuntu 20.04 LTS

Instance Type: t3.medium

Security Group: Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS) 

# Amazon RDS 

* Purpose: Managed relational database service.

* Database Engine: PostgreSQL

* Configuration: 

Instance Class: db.t3.micro

Storage Type: General Purpose (SSD)

Backup: Enabled 

# Amazon S3 

* Purpose: Object storage for data backup and archiving.

* Bucket Name: my-s3-bucket

* Configuration:

Versioning: Enabled

Lifecycle Policies: Transition to Glacier after 1 year 

Setting Up 

# EC2 Setup 

1. Go to the EC2 Dashboard. 

2. Launch a new instance. 

3. Choose the appropriate AMI and instance type. 

4. Configure instance details, add storage, and configure security groups. 

5. Launch and connect to the instance. 

# RDS Setup 

1. Go to the RDS Dashboard. 

2. Create a new database instance. 

3. Choose PostgreSQL as the engine and configure the instance settings. 

4. Configure backups and monitoring. 

5. Launch and connect to the database. 

# S3 Setup 

1. Go to the S3 Dashboard. 

2. Create a new bucket. 

3. Configure bucket settings and permissions. 

4. Upload files and configure lifecycle policies. 

# IAM Roles and Permissions 

Ensure that appropriate IAM roles and policies are set up to provide necessary permissions to your EC2 instances and other AWS services. 

 

# Security Best Practices 

* Regularly update your instances and databases. 

* Use IAM roles and policies to restrict access. 

* Enable encryption for data at rest and in transit. 

* Set up CloudWatch monitoring and alerts. 

# Resources 

* AWS EC2 Documentation 

* AWS RDS Documentation 

* AWS S3 Documentation 

 




Docker 

# Docker Documentation 

# Overview 

This document provides an overview of how to use Docker for containerizing your application. 

 

# Dockerfile 

Here is an example Dockerfile for a Python application: 

``` 

# Use the official Python image from the Docker Hub 

FROM python:3.11-slim 

 

# Set the working directory 

WORKDIR /app 

 

# Copy the requirements file and install dependencies 

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt 

 

# Copy the rest of the application code 

COPY . . 

 

# Expose the port on which the app will run 

EXPOSE 8000 

 

# Define the command to run the application 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 

``` 

 
