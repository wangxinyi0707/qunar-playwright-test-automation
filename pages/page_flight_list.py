"""航班列表页（flight.qunar.com/site/oneway_list.htm）页面对象

注意：航班数据接口在本环境（headless/反爬）下偶发返回空，需 wait_for_flights 重试。
"""
import allure

from pages import (
    FLIGHT_BOOK_BTN,
    FLIGHT_LIST_CONTAINER,
    FLIGHT_LIST_EMPTY,
    FLIGHT_LIST_ROW,
    FLIGHT_PRICE,
)
from pages.basepage import BasePage


class FlightListPage(BasePage):
    def wait_for_flights(self, timeout: int = 30000) -> bool:
        """等待航班列表出现（配合接口 Mock 稳定渲染；真实环境下空态时用例会失败）"""
        return self.is_visible(FLIGHT_LIST_CONTAINER, timeout)

    def has_no_flights(self) -> bool:
        """是否出现空态提示（暂无符合条件的机票信息）"""
        return self.is_visible(FLIGHT_LIST_EMPTY, 5000)

    def is_list_url(self, from_code: str = "", to_code: str = "") -> bool:
        """是否在航班列表页：URL 含 fromCode / toCode 查询参数

        （去哪儿城市代码可能是机场级 PEK/PKX，故默认只断言参数存在）
        """
        url = self.page.url
        if "fromCode=" not in url or "toCode=" not in url:
            return False
        if from_code and from_code not in url:
            return False
        if to_code and to_code not in url:
            return False
        return True

    @allure.step("展开第一个航班的价格舱位")
    def expand_first_price(self, timeout: int = 15000):
        """点击第一个航班的价格，展开舱位列表（预订按钮出现在舱位内）"""
        self.page.locator(FLIGHT_LIST_ROW).first.locator(FLIGHT_PRICE).click(timeout=timeout)

    @allure.step("点击第一个航班的预订按钮")
    def click_book(self, timeout: int = 15000):
        """点击第一个航班的「预订」按钮（会新开标签页）"""
        self.page.locator(FLIGHT_LIST_ROW).first.locator(FLIGHT_BOOK_BTN).click(timeout=timeout)
