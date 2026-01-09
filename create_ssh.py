import subprocess
import sys

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"

SSH_PATH="$HOME/.ssh/"

def intro():
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}SSH CONFIGURATOR{COLOR_RESET}\n-----")
    print("\nThis configurator aims to facilitate the SSH onboarding from creating keys to easing SSH config, agent and usage.")

def warning_ssh_password():
    print(f"\n{COLOR_RED}{COLOR_BLINK}!!! WARNING !!!{COLOR_RESET}\n")
    print(f"{COLOR_RED}If you set a password for your SSH key, you will need to enter it each time you use the key unless you use an SSH agent.{COLOR_RESET}")

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


def main():
    intro()
    check_ssh_path()
    choice = ""
    while choice not in ["wsl", "vps", "windows"]:
        choice = input("Choose your current environment target for ssh configuration (vps, wsl, windows): ")
    
    if choice == "wsl":
        config_wsl()
    elif choice == "vps":
        pass
    else:
        pass


if __name__ == "__main__":
    main()