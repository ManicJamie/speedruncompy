import logging
from src import auth
from src import GetSession

from secret import LOW_USERNAME, LOW_PASSWORD, SESSID
from src.api import SpeedrunComPy

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

print(auth.login_PHPSESSID(SESSID))

response = GetSession().perform()
print(response["session"]["signedIn"])

csrf = auth.get_CSRF()
print(csrf)

api2 = SpeedrunComPy("Test")

response = GetSession(_api=api2).perform()
print(response["session"]["signedIn"])