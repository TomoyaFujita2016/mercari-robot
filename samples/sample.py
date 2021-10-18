import time

import requests
from mercari_purchase_bot import Robot

auth = {"email": "banno2658@gmail.com", "password": "2658banno"}
# auth = {"email": "game.happy7721@gmail.com", "password": "KapiparA0720"}
bot = Robot(auth)
if not bot.is_logged_in():
    print(bot.login())


# s = time.time()
# bot.buy_this("m17763563685", is_test=True)
# e = time.time()
# print(f"{e - s} sec")
# time.sleep(10)


session = requests.session()
for cookie in bot.web_adapter.driver.get_cookies():
    print(f"{cookie['name']}: {cookie['value']}")
    session.cookies.set(cookie["name"], cookie["value"])

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {"User-Agent": ua}
url = "https://www.mercari.com/jp/mypage/"
resp = session.get(url, headers=headers)
