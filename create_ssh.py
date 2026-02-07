import subprocess
import sys
import os
import re

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"

SSH_PATH="$HOME/.ssh/"
DEFAULT_VPS_IP = ""
USER_VPS_NAME = ""
WSL_SSH_KEY_NAME = "id_"

def intro():
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIGURATOR{COLOR_RESET}\n-----")
    print("\nThis configurator aims to facilitate the SSH onboarding from creating keys to easing SSH config, agent and usage.")

def check_ssh_path():
    """Check and confirm the SSH path."""
    print(f"-----\n{COLOR_RED}{COLOR_BLINK}!!! IMPORTANT !!!{COLOR_RESET}\n-----")
    current_path = subprocess.run(f"echo {SSH_PATH}", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"\nYour current SSH path is: {COLOR_GREEN}{current_path}{COLOR_RESET}")
    print(f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to confirm, or type {COLOR_RED}any key + ENTER{COLOR_RESET} to abort.")
    choice = input()
    if choice != "":
        print(f"{COLOR_RED}Aborting SSH configurator. Please check the SSH_PATH variable in the script.{COLOR_RESET}")
        sys.exit(0)

def config_wsl():
    """
    Config script for WSL
    """
    global DEFAULT_VPS_IP, WSL_SSH_KEY_NAME, USER_VPS_NAME
    
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FOR WSL{COLOR_RESET}\n-----")
    
    # Get VPS IP
    print(f"\n{COLOR_GREEN}Enter the IP address of your VPS:{COLOR_RESET}")
    print(f"(This information can be found in Hostinger)")
    print(f"{COLOR_RED}WARNING: Make sure to enter the correct IP address, as it will be used to connect to your VPS via SSH.{COLOR_RESET}")
    print(f"(e.g. 192.168.1.1 or 203.0.113.0)")
    DEFAULT_VPS_IP = input(": ").strip()
    while not DEFAULT_VPS_IP:
        print(f"{COLOR_RED}IP address cannot be empty.{COLOR_RESET}")
        DEFAULT_VPS_IP = input(": ").strip()
    
    # Get SSH key name
    while True:
        print(f"\n{COLOR_GREEN}Enter your SSH key name:{COLOR_RESET}")
        print(f"(Only lowercase letters and underscores allowed)")
        ssh_name = input(": ").strip()
        
        # Strip id_ prefix if user includes it
        if ssh_name.startswith("id_"):
            ssh_name = ssh_name[3:]
        
        # Validate: only lowercase letters and underscores
        if ssh_name and re.match(r'^[a-z_]+$', ssh_name):
            WSL_SSH_KEY_NAME = f"id_{ssh_name}"
            print(f"SSH key will be: {COLOR_GREEN}{WSL_SSH_KEY_NAME}{COLOR_RESET}")
            break
        else:
            print(f"{COLOR_RED}Invalid name. Use only lowercase letters and underscores.{COLOR_RESET}")
    
    # Get VPS username
    print(f"\n{COLOR_RED}Enter your VPS username:{COLOR_RESET}")
    print(f"(WARNING: This user must be already set up on the VPS before running this script)")
    USER_VPS_NAME = input(": ").strip()
    while not USER_VPS_NAME:
        print(f"{COLOR_RED}Username cannot be empty.{COLOR_RESET}")
        USER_VPS_NAME = input(": ").strip()
    
    # Get distant server username (for SSH key paths)
    print(f"\n{COLOR_GREEN}Enter your username on the distant server (for SSH key paths):{COLOR_RESET}")
    print(f"(This is typically your local username on the machine running this script)")
    distant_user = input(": ").strip()
    while not distant_user:
        print(f"{COLOR_RED}Username cannot be empty.{COLOR_RESET}")
        distant_user = input(": ").strip()
    
    # Read config template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "ssh_config", "wsl", "config")
    
    try:
        with open(template_path, 'r') as f:
            config_content = f.read()
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Template config file not found at {template_path}{COLOR_RESET}")
        sys.exit(1)
    
    # Replace placeholders
    config_content = config_content.replace("{DEFAULT_VPS_IP}", DEFAULT_VPS_IP)
    config_content = config_content.replace("{USER_VPS_NAME}", USER_VPS_NAME)
    config_content = config_content.replace("{USER}", distant_user)
    config_content = config_content.replace("ssh_wsl_github", WSL_SSH_KEY_NAME)
    
    # Prepare SSH directory and config path
    ssh_dir = os.path.expanduser("~/.ssh")
    ssh_config_path = os.path.join(ssh_dir, "config")
    
    # Create ~/.ssh directory if it doesn't exist
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    
    # Create backup if config file already exists
    if os.path.exists(ssh_config_path):
        backup_path = f"{ssh_config_path}.backup"
        subprocess.run(["cp", ssh_config_path, backup_path])
        print(f"\n{COLOR_GREEN}✓ Backup created at: {backup_path}{COLOR_RESET}")
    
    # Write new config
    with open(ssh_config_path, 'w') as f:
        f.write(config_content)
    
    # Set proper permissions
    os.chmod(ssh_config_path, 0o600)
    
    print(f"\n{COLOR_GREEN}✓ SSH config successfully created at: {ssh_config_path}{COLOR_RESET}")
    print(f"\nConfiguration summary:")
    print(f"  VPS IP: {DEFAULT_VPS_IP}")
    print(f"  VPS User: {USER_VPS_NAME}")
    print(f"  SSH Key: {WSL_SSH_KEY_NAME}")
    print(f"  Distant User: {distant_user}")


def main():
    intro()
    check_ssh_path()
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Choose your current environment target for ssh configuration\nType 1 for WSL\nType 2 for VPS\n: ").strip()
    
    if choice == "1": # WSL
        config_wsl()
    elif choice == "2": # VPS
        pass
        print("VPS configuration is not implemented yet. Stay tuned for the next release.")
    else:
        pass
        print("Not Recognized choice [1 or 2]. Relaunch the script.")
        sys.exit(1)


if __name__ == "__main__":
    main()