#!/usr/bin/env python3
import subprocess
import sys
import shutil
import random
from fake_useragent import UserAgent

# Fallback list of user agents
FALLBACK_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # ... add local list of user agents here
]
def get_random_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        # Fallback to local list if fake-useragent fails
        return random.choice(FALLBACK_USER_AGENTS)

def modify_http_lua(http_lua_path, backup_path, user_agent):
    try:
        shutil.copy(http_lua_path, backup_path)
        with open(http_lua_path, 'r') as file:
            lines = file.readlines()
        with open(http_lua_path, 'w') as file:
            for line in lines:
                if "USER_AGENT = stdnse.get_script_args" in line and not line.strip().startswith("--"):
                    file.write(f'--{line}')
                    file.write(f"USER_AGENT  = stdnse.get_script_args('http.useragent') or \"{user_agent}\"\n")
                else:
                    file.write(line)
        print("http.lua has been modified.")
    except Exception as e:
        print(f"Error modifying http.lua: {e}")
        sys.exit(1)

def restore_http_lua(http_lua_path, backup_path):
    try:
        shutil.move(backup_path, http_lua_path)
    except Exception as e:
        print(f"Error restoring http.lua: {e}")
        sys.exit(1)

def run_tool_with_user_agent(tool_name, tool_args):
    try:
        user_agent = get_random_user_agent()
        tool_command = [tool_name, *tool_args]

        if tool_name == "nmap":
            http_lua_path = "/usr/share/nmap/nselib/http.lua"
            backup_path = http_lua_path + ".backup"
            modify_http_lua(http_lua_path, backup_path, user_agent)
            try:
                subprocess.run(tool_command, check=True)
            finally:
                restore_http_lua(http_lua_path, backup_path)
        else:
            user_agent_option = "--user-agent" if tool_name in ["wget", "sqlmap", "feroxbuster"] else "-A"
            tool_command.insert(1, user_agent_option)
            tool_command.insert(2, user_agent)
            subprocess.run(tool_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {tool_name}: {e}")
    except Exception as e:
        print(f"Unexpected error with {tool_name}: {e}")
        sys.exit(1)

def run_enumeration(target):
    tools_to_install = [
        "seclists", "curl", "dnsrecon", "enum4linux", "feroxbuster",
        "gobuster", "impacket-scripts", "nbtscan", "nikto", "nmap",
        "onesixtyone", "oscanner", "redis-tools", "smbclient", "smbmap",
        "snmp", "sslscan", "sipvicious", "tnscmd10g", "whatweb", "wkhtmltopdf"
    ]
    print("Checking and installing required tools...")
    subprocess.run(["sudo", "apt", "install", "-y"] + tools_to_install)

    print("Running Autorecon on target...")
    subprocess.run(["autorecon", target])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cleanup_crew.py <command> <target>")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    supported_tools = ["nmap", "curl", "wget", "sqlmap", "ffuf", "feroxbuster", "nikto", "gobuster"]
    if command == "enum":
        run_enumeration(args[0])
    elif command in supported_tools:
        run_tool_with_user_agent(command, args)
    else:
        print(f"Unsupported command: {command}. Supported commands are 'enum', {', '.join(supported_tools)}.")
