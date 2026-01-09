import subprocess
import sys

# ! This group name has been set at the begining, to allow all users to write on all files, regardless of the current file perms.
SHARED_GROUP_NAME = "sharedgrp"

def intro():
    print("-----\n\033[92m\033[5mWelcome to the New User Configurator\033[0m\n-----")
    # print("This configurator will help you configure git crucial settings.\n")

def check_root():
    ss = subprocess.run(["whoami"], capture_output=True, text=True)
    username = ss.stdout.strip()
    # print(f"The current user is : {ss.stdout.strip()}")
    if username != "root":
        print("This Python script is supposed to be run as `root`. Please login with `root` user")
        sys.exit(1)

def create_new_user():
    new_username = ""
    while not new_username.islower():
        new_username = input("Enter a new UNIX user. Lowercase characters only: ")

    # Creating user
    subprocess.run(["adduser", new_username])

    # Adding the new created user to `sudo` group
    add_sudo = ""
    while add_sudo not in ["y", "n"]:
        add_sudo = input(f"Do you want to add {new_username} in sudo group (y/n): ")
    if add_sudo == 'y':
        subprocess.run(["usermod", "-aG", "sudo", new_username])

    # Adding the new created user to Docker group
    add_docker = ""
    while add_docker not in ["y", "n"]:
        add_docker = input(f"Do you want to add {new_username} in docker group (Highly recommanded): (y/n)")
    if add_docker == "y":
        subprocess.run(["usermod", "-aG", "docker", new_username])

    # Add user to SHARED_GROUP_NAME
    subprocess.run(["usermod", "-aG", SHARED_GROUP_NAME, new_username])

    print(f"-----\n\033[92m\033[5mUser {new_username} has been created, with{"out" if add_sudo == 'n' else ""} sudo perms, with{"out" if add_docker == 'n' else ""} docker perms, and it's part of the {SHARED_GROUP_NAME} group.\033[0m\n-----")

def main():
    intro()
    check_root()
    create_new_user()

if __name__ == "__main__":
    main()