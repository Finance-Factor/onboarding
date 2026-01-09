import subprocess

def intro():
    print("-----\nWelcome to the Git Configurator\n-----")
    print("This configurator will help you configure git crucial settings.\n")
    
def configure_username():
    print("-----\n\033[92m\033[5mGIT USERNAME CONFIGURATION\033[0m\n-----")
    print("\033[91m\033[5mIMPORTANT: This username will be used to sign your commits. It is recommended to use the same username as your GitHub account.\033[0m")
    username = input("Enter the name you want to sign your commits with: ")
    subprocess.run(["git", "config", "--global", "user.name", username])

    print(f"Your username has been configured as \033[91m\033[5m{username}\033[0m")

def configure_email():
    print("-----\n\033[92m\033[5mGIT EMAIL CONFIGURATION\033[0m\n-----")
    print("\033[91m\033[5mIMPORTANT: This email will be used to sign your commits. It must match the email associated with your GitHub account.\033[0m")
    email = input("Enter the email you want to sign your commits with: ")
    subprocess.run(["git", "config", "--global", "user.email", email])

    print(f"Your email has been configured as \033[91m\033[5m{email}\033[0m")

def main():
    intro()
    configure_username()
    configure_email()

if __name__ == "__main__":
    main()
