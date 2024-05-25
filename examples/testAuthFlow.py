import logging
from speedruncompy import auth
from speedruncompy import GetSession

from secret import LOW_USERNAME, LOW_PASSWORD, SESSID
from speedruncompy.api import SpeedrunClient

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

print(auth.login_PHPSESSID(SESSID))

response = GetSession().perform()
print(response["session"]["signedIn"])

csrf = auth.get_CSRF()
print(csrf)

api2 = SpeedrunClient("Test")

response = GetSession(_api=api2).perform()
print(response["session"]["signedIn"])