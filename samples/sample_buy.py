import json
import time

import requests
from bs4 import BeautifulSoup
from mercari_purchase_bot import Robot
from requests_html import HTMLSession
from web_adapter.materials import URL

auth = {"email": "banno2658@gmail.com", "password": "2658banno"}
# auth = {"email": "game.happy7721@gmail.com", "password": "KapiparA0720"}
bot = Robot(auth)
if not bot.is_logged_in():
    print(bot.login())

# s = time.perf_counter()
# e = time.perf_counter()
# print(e - s, "sec")


session = requests.session()
for cookie in bot.web_adapter.driver.get_cookies():
    print(f"{cookie['name']}: {cookie['value']}")
    session.cookies.set(cookie["name"], cookie["value"])

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {"User-Agent": ua}


def make_param(input_dict):
    return {
        "operationName": "TransactionsBuyPurchase",
        "variables": {"input": input_dict},
        "query": "mutation TransactionsBuyPurchase($input: TransactionsBuyInput !) {\n transactionsBuy(input: $input) {\n data {\n id\n paidMethod\n price\n paymentFee\n paidPrice\n __typename\n }\n error {\n code\n message\n __typename\n }\n __typename\n }\n}\n",
    }


def buy(item_id):
    buy_url = URL(f"https://www.mercari.com/jp/transaction/buy/{item_id}/")
    bot.web_adapter.get_page(buy_url)
    resp = bot.web_adapter.get_html()
    # print(resp.content)
    # resp = session.get(buy_url, headers=headers)
    # print(resp.text)
    soup = BeautifulSoup(resp.content, "lxml")
    params = soup.select_one("#__NEXT_DATA__")
    params = str(params)[108:-9]
    #print(json.loads(params))
    print(params)


buy("m54715580292")
