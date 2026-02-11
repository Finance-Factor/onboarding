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
DEFAULT_VPS_IP = ""
SSH_SHORTCUT_NAME = ""
SSH_KEY_FILENAME = "id_"
USER_VPS_NAME = ""
WINDOWS_USERNAME = ""
SSH_PATH = "$HOME/.ssh/"
LOCAL_USER = ""
KEY_TYPE = "ed25519"
SSH_DIR = ""
SSH_CONFIG_PATH = ""


def intro():
    """
    Display the introduction message for the SSH configurator.
    """
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIGURATOR{COLOR_RESET}\n-----")
    print(
        "\nThis configurator aims to facilitate the SSH onboarding from creating keys to easing SSH config, agent and usage."
    )


def check_ssh_path():
    """
    Check and confirm the SSH path.
    """
    print(f"-----\n{COLOR_RED}{COLOR_BLINK}!!! IMPORTANT !!!{COLOR_RESET}\n-----")
    current_path = subprocess.run(
        f"echo {SSH_PATH}", shell=True, capture_output=True, text=True
    ).stdout.strip()
    print(f"\nYour current SSH path is: {COLOR_GREEN}{current_path}{COLOR_RESET}")
    print(
        f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to confirm, or type {COLOR_RED}any key + ENTER{COLOR_RESET} to abort."
    )
    choice = input()
    if choice != "":
        print(
            f"{COLOR_RED}Aborting SSH configurator. Please check the SSH_PATH variable in the script.{COLOR_RESET}"
        )
        sys.exit(0)


def check_root():
    """
    Check if the script is being run as root and warn the user.
    """
    print(
        f"\n{COLOR_RED}WARNING: Running as root is not recommended for SSH configuration.{COLOR_RESET}"
    )
    if os.getuid() == 0:
        print(
            f"{COLOR_RED}Error: This script cannot be run as root. Please run as a regular user.{COLOR_RESET}"
        )
        sys.exit(1)


def get_default_vps_ip():
    """
    Prompt the user to enter the IP address of their VPS and validate it.
    """
    global DEFAULT_VPS_IP

    print(f"\n{COLOR_GREEN}Enter the IP address of your VPS:{COLOR_RESET}")
    print(f"(This information can be found in Hostinger)")
    print(
        f"{COLOR_RED}WARNING: Make sure to enter the correct IP address, as it will be used to connect to your VPS via SSH.{COLOR_RESET}"
    )
    print(f"(e.g. 192.168.1.1 or 203.0.113.0)")

    while True:
        DEFAULT_VPS_IP = input(": ").strip()
        # Check regex for ipv4
        if re.match(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            DEFAULT_VPS_IP,
        ):
            break
        else:
            print(
                f"{COLOR_RED}Invalid IPv4 address. Please enter a valid IP (e.g. 192.168.1.1){COLOR_RESET}"
            )


def get_ssh_shortcut_name():
    """
    Prompt the user to enter the SSH shortcut name for their VPS and validate it.
    """
    global SSH_SHORTCUT_NAME

    print(
        f"\n{COLOR_GREEN} Enter a name for your SSH shortcut (e.g. myvps):{COLOR_RESET}"
    )
    print(
        f"{COLOR_RED}WARNING: This name will be used as the SSH host alias in your config, so choose something memorable, short and easy to type.{COLOR_RESET}"
    )
    print(f"(Only lowercase letters allowed, no spaces or special characters)")
    print(
        f"{COLOR_RED}The shortcut will allow you to connect to your VPS with: ssh {COLOR_GREEN}your_ssh_shortcut{COLOR_RESET}{COLOR_RED} instead of ssh user@{DEFAULT_VPS_IP}{COLOR_RESET}"
    )

    SSH_SHORTCUT_NAME = input(": ").strip()

    while not SSH_SHORTCUT_NAME or not SSH_SHORTCUT_NAME.islower():
        print(
            f"{COLOR_RED}Shortcut name cannot be empty or other than pure lowercase.{COLOR_RESET}"
        )
        SSH_SHORTCUT_NAME = input(": ").strip()


def get_ssh_key_filename():
    """
    Prompt the user to enter a name for their SSH key and validate it.
    """
    global SSH_KEY_FILENAME

    # ! Get the variable SSH_KEY_FILENAME
    # * GLOBAL
    while True:
        print(f"\n{COLOR_GREEN}Enter your SSH key name:{COLOR_RESET}")
        print(
            f"{COLOR_RED}WARNING: This name needs, idealy, to be short and clearly identifiable.{COLOR_RESET}"
        )
        print(f"(Only lowercase letters and underscores allowed)")
        print(
            f"{COLOR_RED}The SSH key will be created in your ~/.ssh/ directory with the name: {COLOR_GREEN}id_yourkeyname{COLOR_RESET}{COLOR_RED} (e.g. id_myvps){COLOR_RESET}"
        )
        ssh_name = input(": ").strip()

        # Strip id_ prefix if user includes it
        if ssh_name.startswith("id_"):
            ssh_name = ssh_name[3:]

        # Validate: only lowercase letters and underscores
        if ssh_name and re.match(r"^[a-z_]+$", ssh_name):
            SSH_KEY_FILENAME = f"id_{ssh_name}"
            print(f"SSH key will be: {COLOR_GREEN}{SSH_KEY_FILENAME}{COLOR_RESET}")
            break
        else:
            print(
                f"{COLOR_RED}Invalid name. Use only lowercase letters and underscores.{COLOR_RESET}"
            )


def get_user_vps_name():
    """
    Prompt the user to enter their VPS username and validate it.
    """
    global USER_VPS_NAME
    # ! Get the variable USER_VPS_NAME
    # * PURE WSL
    print(f"\n{COLOR_RED}Enter your VPS UNIX session username:{COLOR_RESET}")
    print(
        f"(WARNING: This user must be already set up on the VPS before running this script)"
    )

    USER_VPS_NAME = input(": ").strip()

    while not USER_VPS_NAME:
        print(f"{COLOR_RED}Username cannot be empty.{COLOR_RESET}")
        USER_VPS_NAME = input(": ").strip()


def get_local_user():
    """
    Prompt the user to enter their local username for the SSH config and validate it.
    """
    global LOCAL_USER

    try:
        default_user = os.getlogin()
    except OSError:
        default_user = os.environ.get("USER", "")

    print(
        f"\n{COLOR_GREEN}Enter your local username (detected: {default_user}):{COLOR_RESET}"
    )
    print(
        f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to use detected username, or type a different username."
    )
    user_input = input(": ").strip()

    if not user_input:
        # User pressed enter, use default
        LOCAL_USER = default_user
        if not LOCAL_USER:
            print(
                f"{COLOR_RED}Error: Could not determine local username. Please specify it manually in global variable LOCAL_USER of this script.{COLOR_RESET}"
            )
            sys.exit(1)
    else:
        # User entered a custom username, confirm it
        print(f"\n{COLOR_GREEN}You entered: {user_input}{COLOR_RESET}")
        print(
            f"Press {COLOR_GREEN}ENTER{COLOR_RESET} to confirm, or type a different username to change."
        )
        confirmation = input(": ").strip()

        if confirmation:
            # User wants to change it
            LOCAL_USER = confirmation
        else:
            # User confirmed
            LOCAL_USER = user_input

    print(f"{COLOR_GREEN}✓ Local user set to: {LOCAL_USER}{COLOR_RESET}")


def create_ssh_key():
    """
    Create SSH key pair using ssh-keygen command and set proper permissions.
    """
    global SSH_KEY_FILENAME, SSH_KEY_PATH, SSH_DIR

    # Create .ssh directory if it doesn't exist and set proper permissions
    SSH_DIR = os.path.expanduser("~/.ssh")
    os.makedirs(SSH_DIR, mode=0o700, exist_ok=True)

    SSH_KEY_PATH = os.path.join(SSH_DIR, SSH_KEY_FILENAME)
    ssh_key_pub_path = f"{SSH_KEY_PATH}.pub"

    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}SSH KEY GENERATION{COLOR_RESET}\n-----")

    print(
        f"{COLOR_RED}{COLOR_BLINK}Your SSH key will need, idealy, to have a passphrase for better security.{COLOR_RESET}"
    )
    print(
        f"{COLOR_GREEN}A SSH passphrase adds an extra layer of security to your SSH key. Even if someone gets access to your private key file, they won't be able to use it without the passphrase.{COLOR_RESET}"
    )
    if os.path.exists(SSH_KEY_PATH) or os.path.exists(ssh_key_pub_path):
        print(
            f"\n{COLOR_RED}WARNING: SSH key already exists at {SSH_KEY_PATH}{COLOR_RESET}"
        )
        overwrite = input(f"Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ["yes", "y"]:
            print(f"{COLOR_GREEN}Using existing SSH key.{COLOR_RESET}")
        else:
            print(f"\n{COLOR_GREEN}Generating new SSH key...{COLOR_RESET}")

            # Build ssh-keygen command
            cmd = ["ssh-keygen", "-t", KEY_TYPE, "-f", SSH_KEY_PATH]

            # Run ssh-keygen
            result = subprocess.run(cmd)

            if result.returncode == 0:
                print(
                    f"\n{COLOR_GREEN}✓ SSH key successfully generated at: {SSH_KEY_PATH}{COLOR_RESET}"
                )
            else:
                print(f"\n{COLOR_RED}Error: Failed to generate SSH key.{COLOR_RESET}")
                sys.exit(1)
    else:
        print(f"\n{COLOR_GREEN}Generating new SSH key...{COLOR_RESET}")

        # Build ssh-keygen command
        cmd = ["ssh-keygen", "-t", KEY_TYPE, "-f", SSH_KEY_PATH]

        # Run ssh-keygen
        result = subprocess.run(cmd)

        if result.returncode == 0:
            print(
                f"\n{COLOR_GREEN}✓ SSH key successfully generated at: {SSH_KEY_PATH}{COLOR_RESET}"
            )
        else:
            print(f"\n{COLOR_RED}Error: Failed to generate SSH key.{COLOR_RESET}")
            sys.exit(1)

    # Set proper permissions
    os.chmod(SSH_KEY_PATH, 0o600)
    if os.path.exists(ssh_key_pub_path):
        os.chmod(ssh_key_pub_path, 0o644)


def configure_ssh_agent():
    """
    Configure SSH agent by starting it and adding the generated key.
    """

    home_dir = os.path.expanduser("~")
    ssh_agent_lines = '\n# Start agent ssh\nssh-add -l >/dev/null 2>&1 || eval "$(ssh-agent -s)" >/dev/null\nexport SSH_ASKPASS_REQUIRE=never\n'

    # Add to both .bashrc and .zshrc if they exist, or create them if they don't
    for rc_file_name in [".bashrc", ".zshrc"]:
        rc_file_path = os.path.join(home_dir, rc_file_name)

        # Create file if it doesn't exist
        if not os.path.exists(rc_file_path):
            print(f"{COLOR_GREEN}Creating {rc_file_name}...{COLOR_RESET}")
            open(rc_file_path, "w").close()
            os.chmod(rc_file_path, 0o644)

        # Read current content
        with open(rc_file_path, "r") as f:
            rc_content = f.read()

        # Check if SSH agent config already exists
        if "Start agent ssh" not in rc_content and "ssh-add -l" not in rc_content:
            with open(rc_file_path, "a") as f:
                f.write(ssh_agent_lines)
            print(
                f"{COLOR_GREEN}✓ SSH agent configuration added to {rc_file_name}{COLOR_RESET}"
            )
        else:
            print(
                f"{COLOR_GREEN}✓ SSH agent configuration already exists in {rc_file_name}{COLOR_RESET}"
            )


def configure_ssh_config(target: str):
    """
    Configure SSH config file by creating a new entry for the VPS connection.
    """
    global SSH_CONFIG_PATH
    # Read config template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "ssh_config", target, "config")

    try:
        with open(template_path, "r") as f:
            config_content = f.read()
    except FileNotFoundError:
        print(
            f"{COLOR_RED}Error: Template config file not found at {template_path}{COLOR_RESET}"
        )
        sys.exit(1)

    # Replace placeholders only for WSL case
    if target == "wsl":
        config_content = config_content.replace("{DEFAULT_VPS_IP}", DEFAULT_VPS_IP)
        config_content = config_content.replace("{USER_VPS_NAME}", USER_VPS_NAME)
        config_content = config_content.replace("{SSH_SHORTCUT_NAME}", SSH_SHORTCUT_NAME)
    
    # Replace placeholders for both VPS and WSL
    config_content = config_content.replace("{SSH_KEY_FILENAME}", SSH_KEY_FILENAME)
    config_content = config_content.replace("{LOCAL_USER}", LOCAL_USER)

    # SSH config path (SSH_DIR already created earlier)
    SSH_CONFIG_PATH = os.path.join(SSH_DIR, "config")

    print(f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FILE{COLOR_RESET}\n-----")

    # Create backup if config file already exists
    if os.path.exists(SSH_CONFIG_PATH):
        backup_path = f"{SSH_CONFIG_PATH}.backup"
        subprocess.run(["cp", SSH_CONFIG_PATH, backup_path])
        print(
            f"{COLOR_RED}Existing SSH config found. Backup created at: {backup_path}{COLOR_RESET}"
        )
        print(
            f"{COLOR_GREEN}You'll need to manually merge the new config with your existing one if you have custom settings. The new config is available at: {backup_path}{COLOR_RESET}"
        )

    # Write new config
    with open(SSH_CONFIG_PATH, "w") as f:
        f.write(config_content)

    # Set proper permissions
    os.chmod(SSH_CONFIG_PATH, 0o600)


def resume_ssh_config(target: str):
    """
    Display summary and next steps after SSH configuration.
    """

    print(
        f"{COLOR_RED}Note: Run 'source ~/.bashrc' or 'source ~/.zshrc' or restart your terminal to activate{COLOR_RESET}"
    )

    print(
        f"\n{COLOR_GREEN}✓ SSH config successfully created at: {SSH_CONFIG_PATH}{COLOR_RESET}"
    )
    print(f"\n{COLOR_GREEN}{COLOR_BLINK}======== CONFIGURATION SUMMARY ========{COLOR_RESET}")
    if target == "wsl":
        print(f"  VPS IP: {DEFAULT_VPS_IP}")
        print(f"  VPS User: {USER_VPS_NAME}")
    print(f"  SSH Key: {SSH_KEY_FILENAME}")
    print(f"  SSH Key Path: {SSH_KEY_PATH}")
    print(f"  Local User: {LOCAL_USER}")

    print(f"\n{COLOR_GREEN}{COLOR_BLINK}======== NEXT STEPS ========{COLOR_RESET}")
    
    if target == "wsl":
        print(f"\n. {COLOR_GREEN}Copy your public key to the VPS provider.{COLOR_RESET}")

    print(f"\n\n. {COLOR_GREEN}Refer to the documentations for the next steps.{COLOR_RESET}")
    print(f"\n{COLOR_GREEN}✓ SSH configuration complete!{COLOR_RESET}\n")


def configure_vscode():
    """
    This helps set up previously generated keys to VS Code Remote - SSH extension by creating a config file in the Windows .ssh directory via symbolic link to WSL .ssh directory.
    """
    global WINDOWS_USERNAME

    print(
        f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}VS CODE SSH CONFIGURATION{COLOR_RESET}\n-----"
    )

    print(f"\n{COLOR_GREEN}Enter your Windows username:{COLOR_RESET}")
    print(f"(This is the username you use to log into Windows)")
    print(
        f"{COLOR_RED} If you are unsure, open a PowerShell terminal and run $env:USERNAME{COLOR_RESET}"
    )

    windows_user = input(": ").strip()
    while not windows_user:
        print(f"{COLOR_RED}Windows username cannot be empty.{COLOR_RESET}")
        windows_user = input(": ").strip()

    WINDOWS_USERNAME = windows_user

    # Create symbolic link to Windows SSH directory
    windows_ssh_path = f"/mnt/c/Users/{windows_user}/.ssh"
    home_dir = os.path.expanduser("~")
    link_name = os.path.join(home_dir, "ssh_windows")

    print(
        f"\n{COLOR_GREEN}Creating symbolic link to Windows SSH directory in home...{COLOR_RESET}"
    )
    cmd = ["ln", "-s", windows_ssh_path, link_name]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(
            f"{COLOR_GREEN}✓ Symbolic link created: {link_name} -> {windows_ssh_path}{COLOR_RESET}"
        )
    else:
        print(f"{COLOR_RED}Error creating symbolic link: {result.stderr}{COLOR_RESET}")
        print(
            f"{COLOR_RED}You may need to create it manually with: ln -s '{windows_ssh_path}' {link_name}{COLOR_RESET}"
        )

    # ! CHECK IF THIS FUNCTION CAN ACCESS THE GLOBAL VARIABLES
    # global DEFAULT_VPS_IP, SSH_KEY_FILENAME, USER_VPS_NAME, SSH_SHORTCUT_NAME

    # Copy SSH keys from WSL to Windows
    print(
        f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}COPYING SSH KEYS TO WINDOWS{COLOR_RESET}\n-----"
    )

    wsl_ssh_dir = os.path.expanduser("~/.ssh")
    wsl_private_key = os.path.join(wsl_ssh_dir, SSH_KEY_FILENAME)
    wsl_public_key = os.path.join(wsl_ssh_dir, f"{SSH_KEY_FILENAME}.pub")

    # Check if keys exist in WSL
    if not os.path.exists(wsl_private_key) or not os.path.exists(wsl_public_key):
        print(
            f"{COLOR_RED}Error: SSH keys not found in WSL at {wsl_private_key}{COLOR_RESET}"
        )
        print(
            f"{COLOR_RED}Please run the WSL configuration first to generate SSH keys.{COLOR_RESET}"
        )
        sys.exit(1)

    # Copy keys to Windows via symlink
    windows_private_key = os.path.join(link_name, SSH_KEY_FILENAME)
    windows_public_key = os.path.join(link_name, f"{SSH_KEY_FILENAME}.pub")

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
    print(
        f"\n-----\n{COLOR_GREEN}{COLOR_BLINK}WINDOWS SSH CONFIG FILE{COLOR_RESET}\n-----"
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "ssh_config", "windows", "config")

    try:
        with open(template_path, "r") as f:
            config_content = f.read()
    except FileNotFoundError:
        print(
            f"{COLOR_RED}Error: Template config file not found at {template_path}{COLOR_RESET}"
        )
        sys.exit(1)

    # Replace placeholders
    config_content = config_content.replace("{DEFAULT_VPS_IP}", DEFAULT_VPS_IP)
    config_content = config_content.replace("{USER_VPS_NAME}", USER_VPS_NAME)
    config_content = config_content.replace("{WINDOWS_USERNAME}", WINDOWS_USERNAME)
    config_content = config_content.replace("{SSH_KEY_FILENAME}", SSH_KEY_FILENAME)
    config_content = config_content.replace("{SSH_SHORTCUT_NAME}", SSH_SHORTCUT_NAME)

    # Write config to Windows SSH directory via symlink
    windows_config_path = os.path.join(link_name, "config")

    # Create backup if config already exists
    if os.path.exists(windows_config_path):
        backup_path = f"{windows_config_path}.backup"
        subprocess.run(["cp", windows_config_path, backup_path])
        print(f"{COLOR_GREEN}✓ Backup created at: {backup_path}{COLOR_RESET}")

    # Write new config
    with open(windows_config_path, "w") as f:
        f.write(config_content)

    # Set proper permissions
    os.chmod(windows_config_path, 0o644)

    print(f"{COLOR_GREEN}✓ Windows SSH config successfully created{COLOR_RESET}")
    print(
        f"\n{COLOR_GREEN}{COLOR_BLINK}=== WINDOWS SSH CONFIGURATION COMPLETE ==={COLOR_RESET}"
    )
    print(f"  SSH keys copied to: C:\\Users\\{WINDOWS_USERNAME}\\.ssh\\")
    print(f"  Config file created: C:\\Users\\{WINDOWS_USERNAME}\\.ssh\\config")

def config_wsl():
    """
    Config script for WSL
    """

    # Defining target name for configure_ssh_config
    target = "wsl"

    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FOR WSL{COLOR_RESET}\n-----")

    get_default_vps_ip()
    get_ssh_shortcut_name()
    get_ssh_key_filename()
    get_user_vps_name()
    get_local_user()
    create_ssh_key()
    configure_ssh_agent()
    configure_ssh_config(target)
    configure_vscode()
    resume_ssh_config(target)

def config_vps():
    """
    Config script for VPS (only get the IP and create a simple config file with it, as we can't generate keys or configure agent on the VPS for the user)
    """

    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIG FOR VPS{COLOR_RESET}\n-----")

    # Defining target name for configure_ssh_config
    target = "vps"

    get_ssh_key_filename()
    get_local_user()
    create_ssh_key()
    configure_ssh_agent()
    configure_ssh_config(target)
    resume_ssh_config(target)

def main():
    intro()
    check_ssh_path()
    check_root()
    choice = ""
    while choice not in ["1", "2"]:
        choice = input(
            "Choose your current environment target for ssh configuration\nType 1 for WSL\nType 2 for Hostinger VPS\n: "
        ).strip()

    if choice == "1":  # WSL
        config_wsl()
    elif choice == "2":  # VPS
        config_vps()
    else:
        print("Not Recognized choice [1 or 2]. Relaunch the script.")
        sys.exit(1)


if __name__ == "__main__":
    main()
