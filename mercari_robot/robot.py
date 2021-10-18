import os
import time
from typing import Optional

from selenium.common.exceptions import ElementClickInterceptedException
from web_adapter import WebAdapter
from web_adapter.materials import URL, ElementHint, Type

from .logger import log


class Robot:
    LOGIN_BASE_URL = URL("https://jp.mercari.com")
    MYPAGE_URL = URL("https://jp.mercari.com/mypage")
    PURCHASE_URL = URL("https://jp.mercari.com/purchase/{item_id}")
    DEFAULT_USER_PROFILE_DIR_NAME = ".user_profiles"
    LOGIN_TIME_LIMIT = 60 * 10  # 10分
    EH = {
        "login_hint": ElementHint(
            "#gatsby-focus-wrapper > div > div > header > mer-navigation-top > nav > mer-navigation-top-menu > mer-menu > mer-navigation-top-menu-item > mer-text",
            Type.CSS_SELECTOR,
        ),
        "login_page_btn": ElementHint(
            "#gatsby-focus-wrapper > div > div > header > mer-navigation-top > nav > mer-navigation-top-menu > mer-navigation-top-menu-item:nth-child(2)",
            Type.CSS_SELECTOR,
        ),
        "login_by_email": ElementHint(
            "#root > div > div > div > main > div > div > div > div > mer-button:nth-child(1)",
            Type.CSS_SELECTOR,
        ),
        "email": ElementHint(
            'input[name="email"]',
            Type.CSS_SELECTOR,
        ),
        "password": ElementHint(
            'input[name="password"]',
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
            'div[data-testid="mypage-top"]',
            Type.CSS_SELECTOR,
        ),
        "purchase_btn": ElementHint(
            'mer-button[intent="primary"]',
            Type.CSS_SELECTOR,
        ),
        "modal": ElementHint(
            "#modal",
            Type.CSS_SELECTOR,
        ),
        "modal_close": ElementHint(
            "#modal > mer-icon-button",
            Type.CSS_SELECTOR,
        ),
        "welcome_dialog": ElementHint(
            "body > mer-information-popup",
            Type.CSS_SELECTOR,
        ),
        "close_dialog_btn": ElementHint(
            "#modal > mer-icon-button",
            Type.CSS_SELECTOR,
        ),
    }

    def __init__(
        self, auth: dict, is_headless=True, user_profile_dir: Optional[str] = None
    ):
        self.auth = auth
        if user_profile_dir is None:
            user_profile_dir = Robot.DEFAULT_USER_PROFILE_DIR_NAME

        # windows, macに対応させるためにos.path.join
        user_data_path: str = os.path.join(
            user_profile_dir, f'_{auth["email"].split("@")[0]}'
        )
        log.debug(f"chrome_profile: {user_data_path}")
        self.web_adapter = WebAdapter(
            is_headless=is_headless, user_data_dir=user_data_path
        )

    def login(self) -> bool:
        log.debug("start login process!")
        self.web_adapter.get_page(Robot.LOGIN_BASE_URL)
        self.web_adapter.click_this(Robot.EH["login_page_btn"])
        self.web_adapter.click_this(Robot.EH["login_by_email"])
        self.web_adapter.input_this(Robot.EH["email"], self.auth["email"])
        self.web_adapter.input_this(Robot.EH["password"], self.auth["password"])
        # self.web_adapter.click_this(Robot.EH["loginbtn"])

        # マイページが表示されるまで待つ
        is_login_succeeded = False
        for i in range(Robot.LOGIN_TIME_LIMIT):
            element = self.web_adapter.find_element(Robot.EH["login_hint"])
            if element is not None:
                hint = element.text
                if hint == "アカウント":
                    is_login_succeeded = True
                    break
            time.sleep(1)
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
        if not is_displayed:
            self.close_welcome_dialog(latency=2)
            is_displayed = self.web_adapter.wait_for_element(
                Robot.EH["mypage_tab"], latency=latency
            )

        log.debug(f"is_logged_in={is_displayed}")
        return is_displayed

    def close_welcome_dialog(self, latency=3):
        element_dialog = self.web_adapter.find_element(
            Robot.EH["welcome_dialog"], latency=latency
        )
        if element_dialog is None:
            return
        shadow_root = self.web_adapter.find_shadow_root(element_dialog)
        self.web_adapter.click_this(
            Robot.EH["close_dialog_btn"], root_element=shadow_root
        )

    def click_buy_btn(self):
        try:
            is_buy = self.web_adapter.click_this(Robot.EH["purchase_btn"])
        except ElementClickInterceptedException:
            log.debug("element click intercepted!")
            is_buy = False
        log.debug(f"is_buy: {is_buy}")
        return is_buy

    def buy_this(self, item_id: str, is_test: bool = False):
        log.debug("In item purchase...")
        # 購入URL
        url = Robot.PURCHASE_URL.fnew(item_id=item_id)
        log.debug(f"Item URL: {url}")
        self.web_adapter.get_page(url)

        if is_test:
            log.debug("test done!(item purchase)")
            return True

        is_buy = self.click_buy_btn()
        if not is_buy:
            # 押せない時にmodal削除を試す
            self.close_welcome_dialog()
            self.click_buy_btn()

        is_buy_success = self.web_adapter.wait_for_element(
            Robot.EH["welcome_dialog"], latency=2
        )

        log.debug(f"done!(item purchase): {is_buy_success}")
        return is_buy_success
