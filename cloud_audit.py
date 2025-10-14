import os
import boto3
import json
from datetime import datetime

# ---------------- AWS CONFIG ---------------- #
REGION = "me-south-1"  # UAE
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# ---------------- FUNCTIONS ---------------- #

def check_s3_buckets():
    s3 = boto3.client(
        's3',
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    result = {"Public Buckets": []}
    try:
        buckets = s3.list_buckets()["Buckets"]
        for bucket in buckets:
            name = bucket["Name"]
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl["Grants"]:
                grantee = grant.get("Grantee", {})
                if grantee.get("URI") == "http://acs.amazonaws.com/groups/global/AllUsers":
                    result["Public Buckets"].append(name)
    except Exception as e:
        result["Error"] = str(e)
    return result

def check_security_groups():
    ec2 = boto3.client(
        'ec2',
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    open_groups = []
    try:
        groups = ec2.describe_security_groups()["SecurityGroups"]
        for g in groups:
            for perm in g.get("IpPermissions", []):
                for iprange in perm.get("IpRanges", []):
                    if iprange.get("CidrIp") == "0.0.0.0/0":
                        open_groups.append(g["GroupName"])
    except Exception as e:
        open_groups.append(f"Error: {str(e)}")
    return {"Open Security Groups": open_groups}

def check_iam_users():
    iam = boto3.client(
        'iam',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    users_no_mfa = []
    try:
        users = iam.list_users()["Users"]
        for user in users:
            mfa = iam.list_mfa_devices(UserName=user["UserName"])
            if len(mfa["MFADevices"]) == 0:
                users_no_mfa.append(user["UserName"])
    except Exception as e:
        users_no_mfa.append(f"Error: {str(e)}")
    return {"Users without MFA": users_no_mfa}

def check_rds_instances():
    rds = boto3.client(
        'rds',
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    public_instances = []
    try:
        instances = rds.describe_db_instances()["DBInstances"]
        for db in instances:
            if db.get("PubliclyAccessible"):
                public_instances.append(db["DBInstanceIdentifier"])
    except Exception as e:
        public_instances.append(f"Error: {str(e)}")
    return {"Public RDS Instances": public_instances}

def check_lambda_functions():
    lambda_client = boto3.client(
        'lambda',
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    risky_functions = []
    try:
        functions = lambda_client.list_functions()["Functions"]
        for fn in functions:
            role = fn["Role"]
            # A simple heuristic: flag roles containing 'Admin'
            if "Admin" in role:
                risky_functions.append(fn["FunctionName"])
    except Exception as e:
        risky_functions.append(f"Error: {str(e)}")
    return {"Risky Lambda Functions": risky_functions}

# ---------------- RUN AUDIT ---------------- #
def cloud_audit():
    return {
        "S3": check_s3_buckets(),
        "EC2": check_security_groups(),
        "IAM": check_iam_users(),
        "RDS": check_rds_instances(),
        "Lambda": check_lambda_functions()
    }

report = cloud_audit()

with open("cloud_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("[+] Cloud audit JSON report saved as 'cloud_report.json'")

# ---------------- GENERATE HTML DASHBOARD ---------------- #
def generate_html(report):
    s3_public = len(report.get("S3", {}).get("Public Buckets", []))
    ec2_open = len(report.get("EC2", {}).get("Open Security Groups", []))
    iam_no_mfa = len(report.get("IAM", {}).get("Users without MFA", []))
    rds_public = len(report.get("RDS", {}).get("Public RDS Instances", []))
    lambda_risky = len(report.get("Lambda", {}).get("Risky Lambda Functions", []))

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cloud Security Audit Dashboard</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f6fa; }}
h1 {{ text-align: center; color: #2f3640; }}
.cards {{ display: flex; justify-content: space-around; margin-bottom: 30px; }}
.card {{ background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; width: 18%; }}
.card h2 {{ margin: 10px 0; }}
table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background-color: #2f3640; color: white; }}
tr:nth-child(even) {{ background-color: #f2f2f2; }}
.risk {{ color: red; font-weight: bold; }}
.safe {{ color: green; font-weight: bold; }}
button {{ background-color: #2f3640; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 20px; }}
button:hover {{ background-color: #40739e; }}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
</head>
<body>

<h1>Cloud Security Audit Dashboard</h1>
<p style="text-align:center;">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

<div style="text-align:center;">
  <button id="downloadPdf">Download PDF</button>
</div>

<div id="reportContent">
<div class="cards">
    <div class="card"><h2>S3</h2><p>Public Buckets</p><h2>{s3_public}</h2></div>
    <div class="card"><h2>EC2</h2><p>Open Security Groups</p><h2>{ec2_open}</h2></div>
    <div class="card"><h2>IAM</h2><p>Users without MFA</p><h2>{iam_no_mfa}</h2></div>
    <div class="card"><h2>RDS</h2><p>Public Instances</p><h2>{rds_public}</h2></div>
    <div class="card"><h2>Lambda</h2><p>Risky Roles</p><h2>{lambda_risky}</h2></div>
</div>

<h2>S3 Buckets</h2>
<table>
<tr><th>Bucket Name</th><th>Status</th></tr>
"""
    if s3_public:
        for bucket in report.get("S3", {}).get("Public Buckets", []):
            html_content += f"<tr><td>{bucket}</td><td class='risk'>Public</td></tr>"
    else:
        html_content += "<tr><td colspan='2' class='safe'>No public buckets</td></tr>"

    html_content += "</table>"

    html_content += "<h2>EC2 Security Groups</h2><table><tr><th>Security Group</th><th>Status</th></tr>"
    if ec2_open:
        for sg in report.get("EC2", {}).get("Open Security Groups", []):
            html_content += f"<tr><td>{sg}</td><td class='risk'>Open to 0.0.0.0/0</td></tr>"
    else:
        html_content += "<tr><td colspan='2' class='safe'>No open security groups</td></tr>"

    html_content += "<h2>IAM Users without MFA</h2><table><tr><th>User</th><th>Status</th></tr>"
    if iam_no_mfa:
        for user in report.get("IAM", {}).get("Users without MFA", []):
            html_content += f"<tr><td>{user}</td><td class='risk'>No MFA</td></tr>"
    else:
        html_content += "<tr><td colspan='2' class='safe'>All users have MFA</td></tr>"

    html_content += "<h2>Public RDS Instances</h2><table><tr><th>Instance</th><th>Status</th></tr>"
    if rds_public:
        for db in report.get("RDS", {}).get("Public RDS Instances", []):
            html_content += f"<tr><td>{db}</td><td class='risk'>Public</td></tr>"
    else:
        html_content += "<tr><td colspan='2' class='safe'>No public RDS instances</td></tr>"

    html_content += "<h2>Risky Lambda Functions</h2><table><tr><th>Function</th><th>Status</th></tr>"
    if lambda_risky:
        for fn in report.get("Lambda", {}).get("Risky Lambda Functions", []):
            html_content += f"<tr><td>{fn}</td><td class='risk'>Risky Role</td></tr>"
    else:
        html_content += "<tr><td colspan='2' class='safe'>No risky Lambda functions</td></tr>"

    html_content += "</table></div>"

    html_content += """
<script>
document.getElementById("downloadPdf").addEventListener("click", function() {
    var element = document.getElementById("reportContent");
    var opt = {
      margin: 0.5,
      filename: 'Cloud_Security_Audit_Report.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save();
});
</script>

</body>
</html>
"""
    with open("cloud_dashboard.html", "w") as f:
        f.write(html_content)
    print("[+] Cloud Security HTML dashboard created as 'cloud_dashboard.html'")
    print("[+] Open it in a browser and click 'Download PDF' to get your report.")

generate_html(report)

