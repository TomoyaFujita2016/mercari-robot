import requests
from bs4 import BeautifulSoup

USERID = "799552435"
url = f"https://www.mercari.com/jp/u/{USERID}/"
CS = "body > div.default-container > section > section > div > section > a"

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {"User-Agent": ua}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text)
items = soup.select(CS)

for item in items:
    print(item.get("href")[10:-1])
