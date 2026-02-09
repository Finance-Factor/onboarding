import subprocess

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"

def intro():
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}Welcome to the Git Configurator{COLOR_RESET}\n-----")
    print("This configurator will help you configure git crucial settings.\n")
    
def configure_username():
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}GIT USERNAME CONFIGURATION{COLOR_RESET}\n-----")
    print(f"{COLOR_RED}IMPORTANT: This username will be used to sign your commits. It is recommended to use the same username as your GitHub account.{COLOR_RESET}")
    username = input("Enter the name you want to sign your commits with: ")
    subprocess.run(["git", "config", "--global", "user.name", username])

    print(f"Your username has been configured as {COLOR_GREEN}{COLOR_BLINK}{username}{COLOR_RESET}")

def configure_email():
    print(f"-----\n{COLOR_GREEN}{COLOR_BLINK}GIT EMAIL CONFIGURATION{COLOR_RESET}\n-----")
    print(f"{COLOR_RED}IMPORTANT: This email will be used to sign your commits. It must match the email associated with your GitHub account.{COLOR_RESET}")
    email = input("Enter the email you want to sign your commits with: ")
    subprocess.run(["git", "config", "--global", "user.email", email])

    print(f"Your email has been configured as {COLOR_GREEN}{COLOR_BLINK}{email}{COLOR_RESET}")

def main():
    intro()
    configure_username()
    configure_email()

if __name__ == "__main__":
    main()
