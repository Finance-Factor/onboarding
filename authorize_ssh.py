import subprocess
import sys
import os
import re

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"

# Global variables
WSL_PUBLIC_KEY = ""
USER_VPS_NAME = ""
AUTHORIZED_FILE_NAME = "authorized_keys"

def check_is_root():
    """
    Check if the script is being run as root and warn the user.
    """
    print(
        f"\n{COLOR_RED}WARNING: This script must run as root on root user.{COLOR_RESET}"
    )
    if os.getuid() != 0:
        print(
            f"{COLOR_RED}Error: This script MUST be run as root.{COLOR_RESET}"
        )
        sys.exit(1)

def get_user_vps_name():
    """
    Prompt the user to enter their VPS username and validate it.
    """
    global USER_VPS_NAME
    print(f"\n{COLOR_RED}Enter your VPS UNIX session username:{COLOR_RESET}")
    print(
        f"(WARNING: This user must be already set up on the VPS before running this script)"
    )

    USER_VPS_NAME = input(": ").strip()

    while not USER_VPS_NAME:
        print(f"{COLOR_RED}Username cannot be empty.{COLOR_RESET}")
        USER_VPS_NAME = input(": ").strip()

def get_public_ssh_key():
    """
    Prompt the user to enter their WSL public SSH key and validate it.
    """
    global WSL_PUBLIC_KEY

    print(f"\n{COLOR_RED}Enter your WSL public SSH key{COLOR_RESET}")
    
    WSL_PUBLIC_KEY = input(": ").strip()
    # Basic validation for SSH public key format
    if not WSL_PUBLIC_KEY.startswith("ssh-"):
        print(f"{COLOR_RED}Error: Invalid SSH public key format.{COLOR_RESET}")
        sys.exit(1)
    

def create_authorized_key():
    """
    Create the file `authorized_keys`
    """

    # Create .ssh directory if it doesn't exist and set proper permissions
    SSH_DIR = os.path.expanduser(f"/home/{USER_VPS_NAME}/.ssh")
    os.makedirs(SSH_DIR, mode=0o700, exist_ok=True)

    # Create file if it does not exists
    AUTHORIZED_KEYS_PATH = os.path.join(SSH_DIR, AUTHORIZED_FILE_NAME)
    
    # Check if file exists and if it contains the key
    if os.path.exists(AUTHORIZED_KEYS_PATH):
        with open(AUTHORIZED_KEYS_PATH, 'r') as f:
            existing_content = f.read()
            if WSL_PUBLIC_KEY in existing_content:
                print(f"{COLOR_GREEN}SSH key already exists in {AUTHORIZED_KEYS_PATH}{COLOR_RESET}")
                return
        
        # File exists but doesn't contain the key, append it
        with open(AUTHORIZED_KEYS_PATH, 'a') as f:
            f.write(f"\n{WSL_PUBLIC_KEY}\n")
        print(f"{COLOR_GREEN}SSH key appended to {AUTHORIZED_KEYS_PATH}{COLOR_RESET}")
    else:
        # File doesn't exist, create it and write the key
        with open(AUTHORIZED_KEYS_PATH, 'w') as f:
            f.write(f"{WSL_PUBLIC_KEY}\n")
        print(f"{COLOR_GREEN}Created {AUTHORIZED_KEYS_PATH} with SSH key{COLOR_RESET}")
    
    # Set proper permissions for the file
    os.chmod(AUTHORIZED_KEYS_PATH, 0o600)
    
    # Set ownership to USER_VPS_NAME:USER_VPS_NAME
    import pwd
    user_info = pwd.getpwnam(USER_VPS_NAME)
    
    # Equivalent to chown user1:user1
    os.chown(AUTHORIZED_KEYS_PATH, user_info.pw_uid, user_info.pw_gid)
    os.chown(SSH_DIR, user_info.pw_uid, user_info.pw_gid)
    
    print(f"{COLOR_GREEN}Permissions and ownership set successfully{COLOR_RESET}")

def main():    
    """
    This script allows to create the file `authorized_keys`
    """
    check_is_root()
    get_user_vps_name()
    get_public_ssh_key()
    create_authorized_key()

if __name__ == "__main__":
    main()