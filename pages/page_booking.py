"""订单填写/预订页（qnf.trade.qunar.com/ns/book/fill）页面对象

说明：真实下单需要有效乘机人证件信息与登录态；支付环节不做（行业惯例止步于生成订单）。
"""
import re
import time
from typing import Optional

import allure

from pages import (
    BOOKING_ADD_PASSENGER,
    BOOKING_CONTACT_NAME,
    BOOKING_CONTACT_PHONE,
    BOOKING_PASSENGER_CERT,
    BOOKING_PASSENGER_NAME,
    BOOKING_SUBMIT,
)
from pages.basepage import BasePage


class BookingPage(BasePage):
    def is_on_booking_page(self) -> bool:
        """是否仍在订单填写页（未提交成功）"""
        return "book/fill" in self.page.url

    def wait_ready(self, timeout: int = 30000) -> bool:
        """等待订单填写页就绪：进入 booking 页且乘机人输入框可操作"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if "book/fill" in self.page.url and self.is_visible(BOOKING_PASSENGER_NAME, 3000):
                return True
            self.page.wait_for_timeout(1000)
        return False

    @allure.step("填写乘机人-{name}")
    def fill_passenger(self, name: str, cert_no: str):
        """填写乘机人姓名与证件号（默认证件类型为身份证）"""
        self.fill(BOOKING_PASSENGER_NAME, name)
        self.fill(BOOKING_PASSENGER_CERT, cert_no)

    def add_passenger(self):
        """添加乘机人"""
        self.click(BOOKING_ADD_PASSENGER)

    @allure.step("填写联系人-{name}")
    def fill_contact(self, name: str, phone: str):
        """填写联系人姓名与手机号"""
        self.fill(BOOKING_CONTACT_NAME, name)
        self.fill(BOOKING_CONTACT_PHONE, phone)

    @allure.step("提交订单")
    def submit_order(self):
        """点击「提交订单」"""
        self.click(BOOKING_SUBMIT)

    def is_order_created(self) -> bool:
        """是否已生成订单：离开订单填写页即视为提交成功（跳转支付/订单详情页）"""
        return not self.is_on_booking_page()

    def get_order_no(self) -> Optional[str]:
        """从页面文本中提取订单号（订单号通常为 10 位以上数字）"""
        text = self.page.evaluate("document.body ? document.body.innerText : ''")
        m = re.search(r"订单号[:：]?\s*(\d{10,})", text)
        return m.group(1) if m else None

    def get_validation_tips(self) -> list:
        """收集提交后出现的校验提示文本（未填写必填项时触发）"""
        tips = []
        for kw in ("请填写", "请输入", "不能为空", "必填"):
            for el in self.page.get_by_text(kw, exact=False).all()[:20]:
                try:
                    if el.is_visible():
                        tips.append(el.inner_text().strip()[:60])
                except Exception:
                    pass
        return list(dict.fromkeys(tips))
