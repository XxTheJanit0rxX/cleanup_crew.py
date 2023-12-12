#!/usr/bin/env python3
import os
import random
import requests
import subprocess
import sys
import shutil

# Define the URL for the user-agent list
user_agent_url = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"

# Function to download and save user-agents list
def download_user_agents(url, save_dir):
    user_agents_file_path = os.path.join(save_dir, 'user-agents.txt')
    
    # Check if the user-agents.txt file already exists
    if os.path.exists(user_agents_file_path):
        print(f"User agents list already exists at {user_agents_file_path}. Using existing file.")
    else:
        response = requests.get(url)
        
        if response.status_code == 200:
            user_agents = response.text.split('\n')
            
            # Create the user_agents directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Save the user-agents.txt file
            with open(user_agents_file_path, 'w') as file:
                file.write('\n'.join(user_agents))
            
            print("User agents list downloaded and saved successfully.")
        else:
            print("Failed to download the user agents list.")

# Function to backup and modify the http.lua file
def modify_http_lua(user_agents_file_path):
    http_lua_path = "/usr/share/nmap/nselib/http.lua"
    backup_path = "/usr/share/nmap/nselib/http.lua.backup"
    # Debugging: Print a message after modification
    print("http.lua has been modified.")

    # Backup the original http.lua file
    shutil.copy(http_lua_path, backup_path)

    with open(user_agents_file_path, 'r') as f:
        random_user_agent = random.choice(f.readlines()).strip()

    # Modify the http.lua file
    with open(http_lua_path, 'r') as file:
        lines = file.readlines()

    with open(http_lua_path, 'w') as file:
        for line in lines:
            if "USER_AGENT = stdnse.get_script_args" in line and not line.strip().startswith("--"):
                file.write(f'--{line}')  # Comment out the original line
                file.write(f"USER_AGENT  = stdnse.get_script_args('http.useragent') or \"{random_user_agent}\"\n")
            else:
                file.write(line)

# Function to restore the original http.lua file
def restore_http_lua():
    http_lua_path = "/usr/share/nmap/nselib/http.lua"
    backup_path = "/usr/share/nmap/nselib/http.lua.backup"
    shutil.move(backup_path, http_lua_path)

# Modify the run_nmap_with_user_agent function
def run_nmap_with_user_agent(user_agents_file, nmap_args):
    modify_http_lua(user_agents_file)  # Modify the http.lua file

    nmap_command = [
        "nmap",
        *nmap_args
    ]

    try:
        subprocess.run(nmap_command, check=True)
   
    finally:
        restore_http_lua()  # Restore the http.lua file

# Function to run Nmap with custom http.user-agent script argument
def run_nmap_with_user_agent(user_agents_file, nmap_args):
    modify_http_lua(user_agents_file)  # Modify the http.lua file

    nmap_command = [
        "nmap",
        *nmap_args  # Only Nmap options and targets, no http.user-agent needed
    ]

    try:
        print("Running Nmap with modified user agent.")
        subprocess.run(nmap_command, check=True)
    finally:
        print("Nmap command executed, restoring http.lua.")
        restore_http_lua()  # Restore the http.lua file
        print("http.lua has been restored to original.")

# Function to run Curl with custom user-agent header
def run_curl_with_user_agent(user_agents_file, curl_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    curl_command = ["curl", "-A", random_user_agent, *curl_args]
    
    try:
        subprocess.run(curl_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Curl: {e}")

# Function to run Wget with custom user-agent header
def run_wget_with_user_agent(user_agents_file, wget_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    wget_command = ["wget", f"--user-agent={random_user_agent}", *wget_args]
    
    try:
        subprocess.run(wget_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Wget: {e}")

# Function to run Sqlmap with custom user-agent
def run_sqlmap_with_user_agent(user_agents_file, sqlmap_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    sqlmap_command = ["sqlmap", "--user-agent", random_user_agent, *sqlmap_args]
    
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Sqlmap: {e}")

# Function to run ffuf with custom User-Agent header
def run_ffuf_with_user_agent(user_agents_file, ffuf_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    ffuf_command = ["ffuf", "-H", f"User-Agent: {random_user_agent}", *ffuf_args]
    
    try:
        subprocess.run(ffuf_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running ffuf: {e}")

# Function to run feroxbuster with custom User-Agent header
def run_feroxbuster_with_user_agent(user_agents_file, feroxbuster_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    feroxbuster_command = ["feroxbuster", "--user-agent", random_user_agent, *feroxbuster_args]
    
    try:
        subprocess.run(feroxbuster_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running feroxbuster: {e}")

# Function to run Nikto with custom user-agent string
def run_nikto_with_user_agent(user_agents_file, nikto_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    nikto_command = ["nikto", "-ask=no", "-useragent", random_user_agent, *nikto_args]
    
    try:
        subprocess.run(nikto_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Nikto: {e}")

# Function to run Gobuster with custom user-agent string
def run_gobuster_with_user_agent(user_agents_file, gobuster_args):
    random_user_agent = random.choice(open(user_agents_file).readlines()).strip()
    gobuster_command = ["gobuster", f"-a {random_user_agent}", *gobuster_args]
    
    try:
        subprocess.run(gobuster_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Gobuster: {e}")

# Function to remove the downloded user_agents file
def cleanup_user_agents_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Deleted user agents directory: {directory}")
    else:
        print(f"User agents directory not found: {directory}")

if __name__ == "__main__":
    user_agents_directory = "user_agents"
    
    # Step 1: Download and save the user-agents.txt file
    download_user_agents(user_agent_url, user_agents_directory)
    
    # Step 2: Extract the command and arguments provided on the command line
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Step 3: Run the appropriate tool with a random user-agent
    if command == "nmap":
        run_nmap_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "curl":
        run_curl_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "wget":
        run_wget_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "sqlmap":
        run_sqlmap_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "ffuf":
        run_ffuf_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "feroxbuster":
        run_feroxbuster_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "nikto":
        run_nikto_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    elif command == "gobuster":
        run_gobuster_with_user_agent(os.path.join(user_agents_directory, 'user-agents.txt'), args)
    else:
        print(f"Unsupported command: {command}. Supported commands are 'nmap', 'curl', 'wget', 'sqlmap', 'ffuf', 'feroxbuster', 'nikto', and 'gobuster'.")

    # Cleanup
    cleanup_user_agents_directory(user_agents_directory)
