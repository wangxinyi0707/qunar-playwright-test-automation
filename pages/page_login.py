"""去哪儿统一登录页页面对象：手机号/密码两种登录方式

登录页地址：user.qunar.com/passport/login.jsp
"""
import allure
from urllib.parse import quote

from pages import (
    LOGIN_AGREEMENT_CHECKBOX,
    LOGIN_BASE_URL,
    LOGIN_CODE_INPUT,
    LOGIN_COUNTRY_CODE_INPUT,
    LOGIN_GET_CODE_BTN,
    LOGIN_PASSWORD_INPUT,
    LOGIN_PASSWORD_SUBMIT,
    LOGIN_PHONE_INPUT,
    LOGIN_PHONE_SUBMIT,
    LOGIN_TAB_PASSWORD,
    LOGIN_TAB_PHONE,
    LOGIN_USERNAME_INPUT,
)
from pages.basepage import BasePage


class LoginPage(BasePage):
    def open_login(self, ret_url: str = "https://flight.qunar.com/"):
        """打开去哪儿统一登录页，ret 为登录成功后的跳转地址"""
        url = f"{LOGIN_BASE_URL}?ret={quote(ret_url, safe='')}"
        self.open(url)

    # ---------- 登录方式切换 ----------
    def switch_to_phone_login(self):
        """切换到「手机号登录/注册」"""
        self.click(LOGIN_TAB_PHONE)

    def switch_to_password_login(self):
        """切换到「密码登录」"""
        self.click(LOGIN_TAB_PASSWORD)

    # ---------- 手机号登录模式 ----------
    @allure.step("输入手机号")
    def fill_phone(self, phone: str, country_code: str = "86"):
        """填写国家区号和手机号"""
        self.fill(LOGIN_COUNTRY_CODE_INPUT, country_code)
        self.fill(LOGIN_PHONE_INPUT, phone)

    @allure.step("点击获取验证码")
    def click_get_code(self):
        """点击「获取验证码」（需配合短信/接口拿到验证码）"""
        self.click(LOGIN_GET_CODE_BTN)

    @allure.step("输入短信验证码")
    def fill_code(self, code: str):
        """填写短信验证码"""
        self.fill(LOGIN_CODE_INPUT, code)

    @allure.step("提交手机号登录")
    def submit_phone_login(self):
        """点击「登录/注册」提交手机号登录"""
        self.click(LOGIN_PHONE_SUBMIT)

    def login_by_phone(self, phone: str, code: str, country_code: str = "86"):
        """手机号 + 验证码一键登录（组合动作）"""
        self.switch_to_phone_login()
        self.fill_phone(phone, country_code)
        self.click_get_code()
        self.fill_code(code)
        self.check_agreement()
        self.submit_phone_login()

    # ---------- 密码登录模式 ----------
    @allure.step("密码登录")
    def login_by_password(self, username: str, password: str):
        """用户名/邮箱/手机号 + 密码登录（组合动作）"""
        self.switch_to_password_login()
        self.fill(LOGIN_USERNAME_INPUT, username)
        self.fill(LOGIN_PASSWORD_INPUT, password)
        self.check_agreement()
        self.click(LOGIN_PASSWORD_SUBMIT)

    # ---------- 其他 ----------
    def check_agreement(self):
        """勾选《去哪儿网用户协议》"""
        self.check(LOGIN_AGREEMENT_CHECKBOX)
