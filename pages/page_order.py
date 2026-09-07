"""机票订单列表页（flight.order.qunar.com/flight）页面对象（需登录态）"""
import allure

from pages import ORDER_LIST_CONTAINER, ORDER_LIST_EMPTY, ORDER_LIST_URL
from pages.basepage import BasePage


class OrderPage(BasePage):
    def open_orders(self):
        """打开「我的机票订单」页（依赖 conftest 注入的 Cookie 登录态）"""
        self.open(ORDER_LIST_URL)

    def has_order_list(self, timeout: int = 10000) -> bool:
        """订单列表是否出现"""
        return self.is_visible(ORDER_LIST_CONTAINER, timeout)

    def is_empty(self) -> bool:
        """是否空态：没有符合条件的订单"""
        return self.is_visible(ORDER_LIST_EMPTY, 5000)

    @allure.step("校验订单-{order_no} 是否存在")
    def has_order(self, order_no: str) -> bool:
        """订单号是否出现在当前订单列表页中"""
        self.logger.info(f"查找订单号: {order_no}")
        text = self.page.evaluate("document.body ? document.body.innerText : ''")
        return order_no in text
