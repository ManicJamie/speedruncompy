"""
Basic script to login a new SRC session & get its session ID. Useful if you do not want to bother adding standard login code to your program & storing a username/password.
"""

from speedruncompy import auth, api
from getpass import getpass

username = input("Enter username: ")
password = getpass("Enter password: ")
auth.login(username, password)

print(api.cookie["PHPSESSID"])