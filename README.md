\# CloudSecAudit


\*\*CloudSecAudit\*\* is a professional Cloud and System Security Audit Tool designed for AWS environments. It helps security professionals, auditors, and DevOps engineers identify misconfigurations and potential security risks across AWS services. The tool generates comprehensive reports in \*\*JSON\*\*, \*\*HTML dashboard\*\*, and \*\*PDF\*\* formats.



---



\## Features



\- ✅ \*\*S3 Bucket Audit\*\* – Detects public S3 buckets.

\- ✅ \*\*EC2 Security Groups Audit\*\* – Identifies open security groups (0.0.0.0/0).

\- ✅ \*\*IAM User Audit\*\* – Checks users without Multi-Factor Authentication (MFA).

\- ✅ \*\*RDS Audit\*\* – Finds publicly accessible RDS instances.

\- ✅ \*\*Lambda Audit\*\* – Detects risky Lambda roles.

\- ✅ \*\*Professional HTML Dashboard\*\* – Interactive and easy to read.

\- ✅ \*\*PDF Export\*\* – Download a complete PDF report for documentation or compliance.



---



\## Prerequisites



\- Python 3.8+

\- AWS credentials with appropriate permissions (via environment variables)

\- Virtual environment recommended



---



\## Installation



1\. Clone the repository:



&nbsp;   ```bash

&nbsp;   git clone https://github.com/s7a7am/CloudSecAudit.git

&nbsp;   cd CloudSecAudit

&nbsp;   ```



2\. Create and activate a virtual environment:



&nbsp;   ```bash

&nbsp;   python -m venv venv

&nbsp;   # Windows

&nbsp;   venv\\Scripts\\activate

&nbsp;   # Linux / macOS

&nbsp;   source venv/bin/activate

&nbsp;   ```



3\. Install required Python packages:



&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```



4\. Set your AWS credentials as environment variables:



&nbsp;   ```bash

&nbsp;   # Windows

&nbsp;   setx AWS\_ACCESS\_KEY "YOUR\_ACCESS\_KEY"

&nbsp;   setx AWS\_SECRET\_KEY "YOUR\_SECRET\_KEY"

&nbsp;   setx AWS\_REGION "YOUR\_REGION"  # e.g., me-south-1



&nbsp;   # Linux / macOS

&nbsp;   export AWS\_ACCESS\_KEY="YOUR\_ACCESS\_KEY"

&nbsp;   export AWS\_SECRET\_KEY="YOUR\_SECRET\_KEY"

&nbsp;   export AWS\_REGION="YOUR\_REGION"

&nbsp;   ```



5\. Run the cloud audit script:



&nbsp;   ```bash

&nbsp;   python cloud\_audit.py

&nbsp;   ```



After execution, you will get:



\- `cloud_report.json` – Detailed JSON report

\- `cloud_dashboard.html` – Interactive HTML dashboard with \*\*Download PDF\*\* option



Open `cloud_dashboard.html` in your browser and click \*\*Download PDF\*\* to save the report.



---



\## Folder Structure



CloudSecAudit/

│

├─ cloud_audit.py # Main cloud audit script

├─ cloud_dashboard.html # Interactive dashboard

├─ cloud_report.json # JSON report

├─ requirements.txt # Dependencies

├─ screenshots/ # Sample screenshots

├─ samples/ # Sample JSON and PDF reports

└─ README.md # Project description



---



\## Security Note



\- Do \*\*NOT\*\* commit AWS access keys to GitHub. Use environment variables instead.

\- Ensure IAM user has \*\*least privilege\*\* required for auditing.



---



\## Contributing



Contributions, issues, and feature requests are welcome!  

Please follow best practices for secure cloud access when testing.



---



\## License



This project is licensed under the MIT License.  



\*\*Author:\*\* s7a7am



