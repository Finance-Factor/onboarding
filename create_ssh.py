import subprocess
import sys
import os
import re

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"

DEFAULT_VPS_IP = "" # ✅
SSH_SHORTCUT_NAME = "" # ✅
WSL_SSH_KEY_NAME = "id_" # ✅
USER_VPS_NAME = "" # ✅
############################################
WINDOWS_USERNAME = "" # ✅
SSH_PATH="$HOME/.ssh/" # ✅⛔
LOCAL_USER = "" # ✅⛔

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

def check_root():
    print(f"\n{COLOR_RED}WARNING: Running as root is not recommended for SSH configuration.{COLOR_RESET}")
    if os.getuid() == 0:
        print(f"{COLOR_RED}Error: This script cannot be run as root. Please run as a regular user.{COLOR_RESET}")
        sys.exit(1)

def config_wsl():
    """
    Config script for WSL
    """

    global DEFAULT_VPS_IP, WSL_SSH_KEY_NAME, USER_VPS_NAME, LOCAL_USER, SSH_SHORTCUT_NAME
    
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FOR WSL{COLOR_RESET}\n-----")
    
    # ! Get the variable DEFAULT_VPS_IP
    # * PURE WSL
    print(f"\n{COLOR_GREEN}Enter the IP address of your VPS:{COLOR_RESET}")
    print(f"(This information can be found in Hostinger)")
    print(f"{COLOR_RED}WARNING: Make sure to enter the correct IP address, as it will be used to connect to your VPS via SSH.{COLOR_RESET}")
    print(f"(e.g. 192.168.1.1 or 203.0.113.0)")
    while True:
        DEFAULT_VPS_IP = input(": ").strip()
        # Check regex for ipv4
        if re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', DEFAULT_VPS_IP):
            break
        else:
            print(f"{COLOR_RED}Invalid IPv4 address. Please enter a valid IP (e.g. 192.168.1.1){COLOR_RESET}")
    
    # ! Get the variable SSH_SHORTCUT_NAME
    # * GLOBAL
    print(f"\n{COLOR_GREEN} Enter a name for your SSH shortcut (e.g. myvps):{COLOR_RESET}")
    print(f"{COLOR_RED}WARNING: This name will be used as the SSH host alias in your config, so choose something memorable, short and easy to type.{COLOR_RESET}")
    SSH_SHORTCUT_NAME = input(": ").strip()
    while not SSH_SHORTCUT_NAME or not SSH_SHORTCUT_NAME.islower():
        print(f"{COLOR_RED}Shortcut name cannot be empty or other than pure lowercase.{COLOR_RESET}")
        SSH_SHORTCUT_NAME = input(": ").strip()
    
    
    # ! Get the variable WSL_SSH_KEY_NAME
    # * GLOBAL
    while True:
        print(f"\n{COLOR_GREEN}Enter your SSH key name:{COLOR_RESET}")
        print(f"{COLOR_RED}WARNING: This name needs, idealy, to be short and clearly identifiable.{COLOR_RESET}")
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
    
    # ! Get the variable USER_VPS_NAME
    # * PURE WSL
    print(f"\n{COLOR_RED}Enter your VPS UNIX session username:{COLOR_RESET}")
    print(f"(WARNING: This user must be already set up on the VPS before running this script)")
    USER_VPS_NAME = input(": ").strip()
    while not USER_VPS_NAME:
        print(f"{COLOR_RED}Username cannot be empty.{COLOR_RESET}")
        USER_VPS_NAME = input(": ").strip()
    
    # ! Get the variable LOCAL_USER
    # * GLOBAL
    # Try to get local username automatically
    try:
        default_user = os.getlogin()
    except OSError:
        default_user = os.environ.get('USER', '')
    
    print(f"\n{COLOR_GREEN}Enter your local username (detected: {default_user}):{COLOR_RESET}")
    print(f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to use detected username, or type a different username.")
    user_input = input(": ").strip()
    
    if not user_input:
        # User pressed enter, use default
        LOCAL_USER = default_user
        if not LOCAL_USER:
            print(f"{COLOR_RED}Error: Could not determine local username. Please specify it manually.{COLOR_RESET}")
            sys.exit(1)
    else:
        # User entered a custom username, confirm it
        print(f"\n{COLOR_GREEN}You entered: {user_input}{COLOR_RESET}")
        print(f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to confirm, or type a different username to change.")
        confirmation = input(": ").strip()
        
        if confirmation:
            # User wants to change it
            LOCAL_USER = confirmation
        else:
            # User confirmed
            LOCAL_USER = user_input
    
    print(f"{COLOR_GREEN}✓ Local user set to: {LOCAL_USER}{COLOR_RESET}")

    
    # Create SSH key
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    
    ssh_key_path = os.path.join(ssh_dir, WSL_SSH_KEY_NAME)
    ssh_key_pub_path = f"{ssh_key_path}.pub"
    
    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}SSH KEY GENERATION{COLOR_RESET}\n-----")
    
    # Check if key already exists
    print(f"{COLOR_RED}Your SSH key will need, idealy, to have a passphrase for better security.{COLOR_RESET}")
    if os.path.exists(ssh_key_path) or os.path.exists(ssh_key_pub_path):
        print(f"\n{COLOR_RED}WARNING: SSH key already exists at {ssh_key_path}{COLOR_RESET}")
        overwrite = input(f"Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ["yes", "y"]:
            print(f"{COLOR_GREEN}Using existing SSH key.{COLOR_RESET}")
        else:
            # Generate new key
            print(f"\n{COLOR_GREEN}Generating new SSH key...{COLOR_RESET}")
            print(f"Choose key type:")
            print(f"  1. ed25519 (recommended, modern and secure)")
            print(f"  2. RSA 4096 (traditional, widely compatible)")
            key_type_choice = input(": ").strip()
            
            if key_type_choice == "1":
                key_type = "ed25519"
                key_bits = None
            else:
                key_type = "rsa"
                key_bits = "4096"
            
            # Get optional comment/email
            comment = input(f"\n{COLOR_GREEN}Enter email/comment for the key (optional, press ENTER to skip):{COLOR_RESET} ").strip()
            
            # Build ssh-keygen command
            cmd = ["ssh-keygen", "-t", key_type, "-f", ssh_key_path]
            if key_bits:
                cmd.extend(["-b", key_bits])
            if comment:
                cmd.extend(["-C", comment])
            
            # Run ssh-keygen
            result = subprocess.run(cmd)
            
            if result.returncode == 0:
                print(f"\n{COLOR_GREEN}✓ SSH key successfully generated at: {ssh_key_path}{COLOR_RESET}")
            else:
                print(f"\n{COLOR_RED}Error: Failed to generate SSH key.{COLOR_RESET}")
                sys.exit(1)
    else:
        # Generate new key
        print(f"\n{COLOR_GREEN}Generating new SSH key...{COLOR_RESET}")
        print(f"Choose key type:")
        print(f"  1. ed25519 (recommended, modern and secure)")
        print(f"  2. RSA 4096 (traditional, widely compatible)")
        key_type_choice = input(": ").strip()
        
        if key_type_choice == "1":
            key_type = "ed25519"
            key_bits = None
        else:
            key_type = "rsa"
            key_bits = "4096"
        
        # Get optional comment/email
        comment = input(f"\n{COLOR_GREEN}Enter email/comment for the key (optional, press ENTER to skip):{COLOR_RESET} ").strip()
        
        # Build ssh-keygen command
        cmd = ["ssh-keygen", "-t", key_type, "-f", ssh_key_path]
        if key_bits:
            cmd.extend(["-b", key_bits])
        if comment:
            cmd.extend(["-C", comment])
        
        # Run ssh-keygen
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"\n{COLOR_GREEN}✓ SSH key successfully generated at: {ssh_key_path}{COLOR_RESET}")
        else:
            print(f"\n{COLOR_RED}Error: Failed to generate SSH key.{COLOR_RESET}")
            sys.exit(1)
    
    # Set proper permissions
    os.chmod(ssh_key_path, 0o600)
    if os.path.exists(ssh_key_pub_path):
        os.chmod(ssh_key_pub_path, 0o644)
    
    # Add key to ssh-agent
    print(f"\n{COLOR_GREEN}Adding SSH key to ssh-agent...{COLOR_RESET}")
    
    # Start ssh-agent if not running
    subprocess.run(["eval $(ssh-agent -s)"], shell=True, capture_output=True)
    
    # Add key to agent
    add_result = subprocess.run(["ssh-add", ssh_key_path], capture_output=True, text=True)
    if add_result.returncode == 0:
        print(f"{COLOR_GREEN}✓ SSH key added to ssh-agent{COLOR_RESET}")
    else:
        print(f"{COLOR_RED}Warning: Could not add key to ssh-agent. You may need to do this manually.{COLOR_RESET}")
    
    # Display public key
    if os.path.exists(ssh_key_pub_path):
        with open(ssh_key_pub_path, 'r') as f:
            pub_key = f.read().strip()
        print(f"\n{COLOR_GREEN}Your public key (copy this to your VPS):{COLOR_RESET}")
        print(f"{COLOR_GREEN}{pub_key}{COLOR_RESET}")

    # Configure ssh_init.sh with the new key
    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}SSH AGENT CONFIGURATION{COLOR_RESET}\n-----")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ssh_init_template = os.path.join(script_dir, "ssh_config", "ssh_init.sh")
    ssh_init_dest = os.path.join(ssh_dir, "ssh_init.sh")
    
    try:
        with open(ssh_init_template, 'r') as f:
            ssh_init_content = f.read()
    except FileNotFoundError:
        print(f"{COLOR_RED}Warning: ssh_init.sh template not found at {ssh_init_template}{COLOR_RESET}")
        ssh_init_content = None
    
    if ssh_init_content:
        # Replace placeholder with actual key name
        ssh_init_content = ssh_init_content.replace("{SSH_KEY_NAME}", WSL_SSH_KEY_NAME)
        
        # Write ssh_init.sh to ~/.ssh/
        with open(ssh_init_dest, 'w') as f:
            f.write(ssh_init_content)
        os.chmod(ssh_init_dest, 0o700)
        print(f"{COLOR_GREEN}✓ SSH agent script created at: {ssh_init_dest}{COLOR_RESET}")
        
        # Add to shell rc file
        home_dir = os.path.expanduser("~")
        zshrc_path = os.path.join(home_dir, ".zshrc")
        bashrc_path = os.path.join(home_dir, ".bashrc")
        
        source_line = f"\n# SSH Agent persistent configuration\nif [ -f ~/.ssh/ssh_init.sh ]; then\n    source ~/.ssh/ssh_init.sh\nfi\n"
        
        # Determine which shell rc file to use
        rc_file = None
        if os.path.exists(zshrc_path):
            rc_file = zshrc_path
            rc_name = ".zshrc"
        elif os.path.exists(bashrc_path):
            rc_file = bashrc_path
            rc_name = ".bashrc"
        
        if rc_file:
            # Check if already added
            with open(rc_file, 'r') as f:
                rc_content = f.read()
            
            if "ssh_init.sh" not in rc_content:
                with open(rc_file, 'a') as f:
                    f.write(source_line)
                print(f"{COLOR_GREEN}✓ SSH agent script added to {rc_name}{COLOR_RESET}")
                print(f"{COLOR_RED}Note: Run 'source ~/{rc_name}' or restart your terminal to activate{COLOR_RESET}")
            else:
                print(f"{COLOR_GREEN}✓ SSH agent script already configured in {rc_name}{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}Warning: Neither .zshrc nor .bashrc found. Add this manually to your shell rc file:{COLOR_RESET}")
            print(f"{source_line}")
    
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
    config_content = config_content.replace("{LOCAL_USER}", LOCAL_USER)
    config_content = config_content.replace("{WSL_SSH_KEY_NAME}", WSL_SSH_KEY_NAME + ".pub")
    config_content = config_content.replace("{SSH_SHORTCUT_NAME}", SSH_SHORTCUT_NAME)
    
    # SSH config path (ssh_dir already created earlier)
    ssh_config_path = os.path.join(ssh_dir, "config")
    
    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FILE{COLOR_RESET}\n-----")
    
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
    print(f"\n{COLOR_GREEN}{COLOR_BLINK}=== CONFIGURATION SUMMARY ==={COLOR_RESET}")
    print(f"  VPS IP: {DEFAULT_VPS_IP}")
    print(f"  VPS User: {USER_VPS_NAME}")
    print(f"  SSH Key: {WSL_SSH_KEY_NAME}")
    print(f"  SSH Key Path: {ssh_key_path}")
    print(f"  Local User: {LOCAL_USER}")
    
    print(f"\n{COLOR_GREEN}{COLOR_BLINK}=== NEXT STEPS ==={COLOR_RESET}")
    print(f"\n1. {COLOR_GREEN}Copy your public key to the VPS:{COLOR_RESET}")
    print(f"   Run: ssh-copy-id -i {ssh_key_path}.pub {USER_VPS_NAME}@{DEFAULT_VPS_IP}")
    print(f"   Or manually add the public key shown above to ~/.ssh/authorized_keys on your VPS")
    print(f"\n2. {COLOR_GREEN}Test your SSH connection:{COLOR_RESET}")
    if SSH_SHORTCUT_NAME:
        print(f"   Run: ssh {SSH_SHORTCUT_NAME}")
    else:
        print(f"   Run: ssh {USER_VPS_NAME}@{DEFAULT_VPS_IP}")
    print(f"\n3. {COLOR_GREEN}If connection fails, check:{COLOR_RESET}")
    print(f"   - SSH service is running on VPS")
    print(f"   - Firewall allows SSH connections (port 22)")
    print(f"   - Public key is correctly added to VPS authorized_keys")
    print(f"\n{COLOR_GREEN}✓ SSH configuration complete!{COLOR_RESET}\n")

def configure_vscode():
    """
    This helps set up previously generated keys to VS Code
    """
    global WINDOWS_USERNAME

    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}VS CODE SSH CONFIGURATION{COLOR_RESET}\n-----")
    
    print(f"\n{COLOR_GREEN}Enter your Windows username:{COLOR_RESET}")
    print(f"(This is the username you use to log into Windows)")
    print(f"{COLOR_RED} If you are unsure, open a PowerShell terminal and run $env:USERNAME{COLOR_RESET}")

    windows_user = input(": ").strip()
    while not windows_user:
        print(f"{COLOR_RED}Windows username cannot be empty.{COLOR_RESET}")
        windows_user = input(": ").strip()
    
    WINDOWS_USERNAME = windows_user
    
    # Create symbolic link to Windows SSH directory
    windows_ssh_path = f"/mnt/c/Users/{windows_user}/.ssh"
    home_dir = os.path.expanduser("~")
    link_name = os.path.join(home_dir, "ssh_windows")
    
    print(f"\n{COLOR_GREEN}Creating symbolic link to Windows SSH directory in home...{COLOR_RESET}")
    cmd = ["ln", "-s", windows_ssh_path, link_name]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{COLOR_GREEN}✓ Symbolic link created: {link_name} -> {windows_ssh_path}{COLOR_RESET}")
    else:
        print(f"{COLOR_RED}Error creating symbolic link: {result.stderr}{COLOR_RESET}")
        print(f"{COLOR_RED}You may need to create it manually with: ln -s '{windows_ssh_path}' {link_name}{COLOR_RESET}")

    # Add config for windows
    global DEFAULT_VPS_IP, WSL_SSH_KEY_NAME, USER_VPS_NAME, SSH_SHORTCUT_NAME
    
    # Copy SSH keys from WSL to Windows
    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}COPYING SSH KEYS TO WINDOWS{COLOR_RESET}\n-----")
    
    wsl_ssh_dir = os.path.expanduser("~/.ssh")
    wsl_private_key = os.path.join(wsl_ssh_dir, WSL_SSH_KEY_NAME)
    wsl_public_key = os.path.join(wsl_ssh_dir, f"{WSL_SSH_KEY_NAME}.pub")
    
    # Check if keys exist in WSL
    if not os.path.exists(wsl_private_key) or not os.path.exists(wsl_public_key):
        print(f"{COLOR_RED}Error: SSH keys not found in WSL at {wsl_private_key}{COLOR_RESET}")
        print(f"{COLOR_RED}Please run the WSL configuration first to generate SSH keys.{COLOR_RESET}")
        sys.exit(1)
    
    # Copy keys to Windows via symlink
    windows_private_key = os.path.join(link_name, WSL_SSH_KEY_NAME)
    windows_public_key = os.path.join(link_name, f"{WSL_SSH_KEY_NAME}.pub")
    
    try:
        # Copy private key
        subprocess.run(["cp", wsl_private_key, windows_private_key], check=True)
        os.chmod(windows_private_key, 0o600)
        print(f"{COLOR_GREEN}✓ Private key copied to Windows{COLOR_RESET}")
        
        # Copy public key
        subprocess.run(["cp", wsl_public_key, windows_public_key], check=True)
        os.chmod(windows_public_key, 0o644)
        print(f"{COLOR_GREEN}✓ Public key copied to Windows{COLOR_RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{COLOR_RED}Error copying keys: {e}{COLOR_RESET}")
        sys.exit(1)
    
    # Read Windows config template
    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}WINDOWS SSH CONFIG FILE{COLOR_RESET}\n-----")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "ssh_config", "windows", "config")
    
    try:
        with open(template_path, 'r') as f:
            config_content = f.read()
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Template config file not found at {template_path}{COLOR_RESET}")
        sys.exit(1)
    
    # Replace placeholders
    config_content = config_content.replace("{DEFAULT_VPS_IP}", DEFAULT_VPS_IP)
    config_content = config_content.replace("{USER_VPS_NAME}", USER_VPS_NAME)
    config_content = config_content.replace("{WINDOWS_USERNAME}", WINDOWS_USERNAME)
    config_content = config_content.replace("{WSL_SSH_KEY_NAME}", WSL_SSH_KEY_NAME)
    config_content = config_content.replace("{SSH_SHORTCUT_NAME}", SSH_SHORTCUT_NAME)
    
    # Write config to Windows SSH directory via symlink
    windows_config_path = os.path.join(link_name, "config")
    
    # Create backup if config already exists
    if os.path.exists(windows_config_path):
        backup_path = f"{windows_config_path}.backup"
        subprocess.run(["cp", windows_config_path, backup_path])
        print(f"{COLOR_GREEN}✓ Backup created at: {backup_path}{COLOR_RESET}")
    
    # Write new config
    with open(windows_config_path, 'w') as f:
        f.write(config_content)
    
    # Set proper permissions
    os.chmod(windows_config_path, 0o644)
    
    print(f"{COLOR_GREEN}✓ Windows SSH config successfully created{COLOR_RESET}")
    print(f"\n{COLOR_GREEN}{COLOR_BLINK}=== WINDOWS SSH CONFIGURATION COMPLETE ==={COLOR_RESET}")
    print(f"  SSH keys copied to: C:\\Users\\{WINDOWS_USERNAME}\\.ssh\\")
    print(f"  Config file created: C:\\Users\\{WINDOWS_USERNAME}\\.ssh\\config")
    print(f"\n{COLOR_GREEN}You can now use SSH from Windows with: ssh {SSH_SHORTCUT_NAME}{COLOR_RESET}\n")



def main():
    intro()
    check_ssh_path()
    check_root()
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Choose your current environment target for ssh configuration\nType 1 for WSL\nType 2 for VPS\n: ").strip()
    
    if choice == "1": # WSL
        # config_wsl()
        configure_vscode()
    elif choice == "2": # VPS
        print("VPS configuration is not implemented yet. Stay tuned for the next release.")
    else:
        print("Not Recognized choice [1 or 2]. Relaunch the script.")
        sys.exit(1)


if __name__ == "__main__":
    main()