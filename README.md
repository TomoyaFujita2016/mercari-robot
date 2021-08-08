# mercari-robot
- RPAで商品購入的な何か
- ログインセッションを保存できるのでreCAPTCHAあっても自動起動✨
## Installation
- `poetry add git+https://github.com/TomoyaFujita2016/mercari-robot#main`

## Sample
```python
import time
from mercari_purchase_bot import Robot

auth = {"email": "hoge", "password": "hoge"}
bot = Robot(auth)
if not bot.is_logged_in():
    print(bot.login())
bot.buy_this("m17763563685", is_test=True)
time.sleep(10)
```
