import os
import time
from typing import Optional

from web_adapter import WebAdapter
from web_adapter.materials import URL, ElementHint, Type

from .logger import log


class Robot:
    LOGIN_URL = URL("https://www.mercari.com/jp/login/")
    MYPAGE_URL = URL("https://www.mercari.com/jp/mypage/")
    PURCHASE_URL = "https://www.mercari.com/jp/transaction/buy/{item_id}/"
    DEFAULT_USER_PROFILE_DIR_NAME = ".user_profiles"
    LOGIN_TIME_LIMIT = 60 * 10  # 10分
    EH = {
        "email": ElementHint(
            "body > div.single-container > main > div > form > div > div:nth-child(1) > input",
            Type.CSS_SELECTOR,
        ),
        "password": ElementHint(
            "body > div.single-container > main > div > form > div > div:nth-child(2) > input",
            Type.CSS_SELECTOR,
        ),
        "loginbtn": ElementHint(
            "body > div.single-container > main > div > form > div > button",
            Type.CSS_SELECTOR,
        ),
        "sms_input": ElementHint(
            "body > div.single-container > main > section > form > div > div > input.input-default",
            Type.CSS_SELECTOR,
        ),
        "sms_btn": ElementHint(
            "body > div.single-container > main > section > form > div > button",
            Type.CSS_SELECTOR,
        ),
        "mypage_tab": ElementHint(
            "body > div.default-container > nav > ol > li:nth-child(2) > span",
            Type.CSS_SELECTOR,
        ),
        "purchase_btn": ElementHint(
            "#__next > div > div.sc-jtRfpW.draXkZ.sc-gzOgki.dqleaH > div > section:nth-child(6) > div > button",
            Type.CSS_SELECTOR,
        ),
    }

    def __init__(self, auth: dict, user_profile_dir: Optional[str] = None):
        self.auth = auth
        if user_profile_dir is None:
            user_profile_dir = Robot.DEFAULT_USER_PROFILE_DIR_NAME

        # windows, macに対応させるためにos.path.join
        user_data_path: str = os.path.join(
            user_profile_dir, f'_{auth["email"].split("@")[0]}'
        )
        log.debug(f"chrome_profile: {user_data_path}")
        self.web_adapter = WebAdapter(is_headless=False, user_data_dir=user_data_path)

    def login(self) -> bool:
        log.debug("start login process!")
        self.web_adapter.get_page(Robot.LOGIN_URL)
        self.web_adapter.input_this(Robot.EH["email"], self.auth["email"])
        self.web_adapter.input_this(Robot.EH["password"], self.auth["password"])
        self.web_adapter.click_this(Robot.EH["loginbtn"])

        # マイページが表示されるまで待つ
        is_login_succeeded = self.web_adapter.wait_for_element(
            Robot.EH["mypage_tab"],
            latency=Robot.LOGIN_TIME_LIMIT,
        )
        return is_login_succeeded

    def do_sms_auth(self, code):
        self.web_adapter.input_this(Robot.EH["sms_input"], code)
        self.web_adapter.click_this(Robot.EH["sms_btn"])

    def is_logged_in(self, latency=1):
        # マイページが表示されているかで判断
        log.debug("is_logged_in ?")
        self.web_adapter.get_page(Robot.MYPAGE_URL)
        is_displayed = self.web_adapter.wait_for_element(
            Robot.EH["mypage_tab"], latency=latency
        )
        log.debug(f"is_logged_in={is_displayed}")
        return is_displayed

    def buy_this(self, item_id: str, is_test: bool = False):
        log.debug("In item purchase...")
        # 購入URL
        url = URL(Robot.PURCHASE_URL, item_id=item_id)
        log.debug(f"Item URL: {url}")
        self.web_adapter.get_page(url)
        if not is_test:
            is_buy = self.web_adapter.click_this(Robot.EH["purchase_btn"])
            log.debug(f"is_buy_success: {is_buy}")
        log.debug("done!(item purchase)")
