import time

import requests

from mercari_robot import Robot

# auth = {"email": "os_inc001@yahoo.co.jp", "password": "os123456"}
# auth = {"email": "banno2658@gmail.com", "password": "2658banno"}
auth = {"email": "pigman11380@gmail.com", "password": "Xylan113"}
bot = Robot(auth, is_headless=False)
if not bot.is_logged_in():
    print(bot.login())

# bot.buy_this("m20804970781", is_test=False)
bot.buy_this("m80388569294", is_test=True)
time.sleep(7000)
