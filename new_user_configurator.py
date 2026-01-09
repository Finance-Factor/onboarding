import subprocess
import sys

# ! This group name has been set at the begining, to allow all users to write on all files, regardless of the file perms.
SHARED_GROUP_NAME = "sharegrp"

def intro():
    print("-----\n\033[92m\033[5mWelcome to the New User Configurator\033[0m\n-----")
    # print("This configurator will help you configure git crucial settings.\n")
    
def check_root():
    ss = subprocess.run(["whoami"], capture_output=True, text=True)
    username = ss.stdout.strip()
    # print(ss.stdout.strip())
    if username is not "root":
        print("This Python script is supposed to be run as `root`. Please login with `root` user")
        sys.exit(1)

def create_new_user():
    new_username = ""
    while not new_username.islower():
        new_username = input("Enter a new UNIX user. Lowercase characters only: ")
    # print(new_username)
    subprocess.run(["adduser", new_username])



def main():
    intro()
    # check_root()
    create_new_user()

if __name__ == "__main__":
    main()
