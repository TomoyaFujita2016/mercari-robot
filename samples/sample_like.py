import time

import requests
from bs4 import BeautifulSoup
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


def like(item_id):
    rsrf_url = f"https://www.mercari.com/jp/items/{item_id}/"

    resp = session.get(rsrf_url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    cs_csrf = "body > div.default-container > section > div.item-button-container.clearfix > div.item-button-left > input[type=hidden]:nth-child(5)"
    cs_is_like = "body > div.default-container > section > div.item-button-container.clearfix > div.item-button-left > button"

    csrf_value = soup.select_one(cs_csrf).get("value")
    like_value = soup.select_one(cs_is_like).get("name")
    print(like_value, csrf_value)
    add_or_delete = None
    if like_value == "like!":
        add_or_delete = "add"
    elif like_value == "unlike":
        add_or_delete = "delete"
    else:
        print("not like or unlike!")
        return
    like_url = f"https://www.mercari.com/jp/like/{add_or_delete}/{item_id}/?__csrf_value={csrf_value}"
    print(like_url)
    resp = session.get(like_url, headers=headers)
    print(resp.status_code)


s = time.perf_counter()
like("m56597077489")
e = time.perf_counter()
print(e - s, "sec")
