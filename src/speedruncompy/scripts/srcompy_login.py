"""
Basic script to login a new SRC session & get its session ID.

Useful if you do not want to bother adding standard login code to your program & storing a username/password.

Especially useful if you have 2FA enabled!
"""

from speedruncompy import auth, api
from getpass import getpass

def main():
    print("This script logs you in & returns a session ID for use with auth.loginPHPSESSID()")
    print("Please note that while your password is excluded from the terminal log, your PHPSESSID is not.")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    loggedin = auth.login(username, password, tokenEntry=True)
    if not loggedin:
        print("Not logged in!")
        exit()

    print(api._default.PHPSESSID)


if __name__ == "__main__":
    main()
