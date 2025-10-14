import os, subprocess, json

def check_firewall():
    result = subprocess.getoutput("netsh advfirewall show allprofiles")
    if "OFF" in result:
        return {"Firewall": "Disabled"}
    return {"Firewall": "Enabled"}

def check_open_ports():
    result = subprocess.getoutput("netstat -an | findstr LISTEN")
    ports = [line for line in result.split("\n") if line.strip()]
    return {"Open Ports": ports[:10]}  # show first 10 for simplicity

def check_users():
    result = subprocess.getoutput("net user")
    users = [line.strip() for line in result.split("\n")[4:-2] if line.strip()]
    return {"User Accounts": users}

def system_audit():
    return {
        "OS": os.name,
        "Firewall": check_firewall(),
        "Open Ports": check_open_ports(),
        "Users": check_users(),
    }

if __name__ == "__main__":
    data = system_audit()
    with open("system_report.json", "w") as f:
        json.dump(data, f, indent=2)
    print("[+] System audit completed. Report saved to system_report.json")
