# CloudSecAudit 🛡️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)  

**CloudSecAudit** is a professional **Cloud and System Security Audit Tool** designed for **AWS environments**. It helps security professionals, auditors, and DevOps engineers identify misconfigurations and potential security risks across AWS services. The tool generates comprehensive reports in **JSON**, **HTML dashboard**, and **PDF** formats.

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Folder Structure](#folder-structure)  
- [Security Note](#security-note)  
- [Contributing](#contributing)  
- [License](#license)

## Features

- ✅ **S3 Bucket Audit** – Detects public S3 buckets.  
- ✅ **EC2 Security Groups Audit** – Identifies open security groups (0.0.0.0/0).  
- ✅ **IAM User Audit** – Checks users without Multi-Factor Authentication (MFA).  
- ✅ **RDS Audit** – Finds publicly accessible RDS instances.  
- ✅ **Lambda Audit** – Detects risky Lambda roles.  
- ✅ **Professional HTML Dashboard** – Interactive and easy to read.  
- ✅ **PDF Export** – Download a complete PDF report for documentation or compliance.

## Prerequisites

- Python **3.8+**  
- AWS credentials with appropriate permissions (via environment variables)  
- Virtual environment recommended

## Installation

**Step 1 — Clone the repository**  
```bash
git clone https://github.com/s7a7am/CloudSecAudit.git
cd CloudSecAudit
```


**Step 2 — Create and activate a virtual environment** 

**Widnows**  
```bash
python -m venv venv
venv\Scripts\activate
```
**Linux / macOS**  
```bash
python -m venv venv
source venv/bin/activate
```


**Step 3 — Install dependencies**  
```bash
pip install -r requirements.txt
```


**Step 4 — Set AWS credentials**

**Windows**  
```bash
setx AWS_ACCESS_KEY "YOUR_ACCESS_KEY"
setx AWS_SECRET_KEY "YOUR_SECRET_KEY"
setx AWS_REGION "YOUR_REGION" # e.g., me-south-1
```
**Linux / macOS**  
```bash
export AWS_ACCESS_KEY="YOUR_ACCESS_KEY"
export AWS_SECRET_KEY="YOUR_SECRET_KEY"
export AWS_REGION="YOUR_REGION"
```


**Step 5 — Run the cloud audit script**  
```bash
python cloud_audit.py
```

## Usage

After running the cloud audit script, you will get:  

- `cloud_report.json` – Detailed JSON report  
- `cloud_dashboard.html` – Interactive HTML dashboard with **Download PDF** option  

Open `cloud_dashboard.html` in your browser and click **Download PDF** to save the report.


## Folder Structure

```
CloudSecAudit/
│
├─ cloud_audit.py # Main cloud audit script
├─ cloud_dashboard.html # Interactive dashboard
├─ cloud_report.json # JSON report
├─ requirements.txt # Dependencies
├─ screenshots/ # Sample screenshots
├─ samples/ # Sample JSON and PDF reports
└─ README.md # Project description
```


## Security Note

- Do **NOT** commit AWS access keys to GitHub. Use environment variables instead.  
- Ensure IAM user has **least privilege** required for auditing.


## Contributing

Contributions, issues, and feature requests are welcome!  

Please follow best practices for secure cloud access when testing.


## License

This project is licensed under the **MIT License**.  

**Author:** s7a7am


