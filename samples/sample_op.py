import time

import requests
from mercari_robot import Robot

# auth = {"email": "os_inc001@yahoo.co.jp", "password": "os123456"}
auth = {"email": "pigman11380@gmail.com", "password": "Xylan113"}
# auth = {"email": "banno2658@gmail.com", "password": "2658banno"}
bot = Robot(auth, is_headless=False)
if not bot.is_logged_in():
    print(bot.login())

try:
    for i in range(120):
        print(f"{i}/120")
        time.sleep(60)
except KeyboardInterrupt:
    pass
