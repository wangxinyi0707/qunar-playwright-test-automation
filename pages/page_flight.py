"""机票搜索页（flight.qunar.com）页面对象：搜索机票（游客可用，无需登录）"""
import allure

from pages import (
    FLIGHT_CITY_FROM,
    FLIGHT_CITY_HOT,
    FLIGHT_CITY_SUGGEST_ROW,
    FLIGHT_CITY_TO,
    FLIGHT_DATE_INPUT,
    FLIGHT_SEARCH_BTN,
    FLIGHT_URL,
)
from pages.basepage import BasePage


class FlightSearchPage(BasePage):
    def open_flight(self):
        """打开机票搜索页"""
        self.open(FLIGHT_URL)

    def _pick_city(self, input_locator: str, city: str):
        """输入城市名并从建议列表点选（优先建议行，兜底热门城市链接）；全部失败仅告警不抛错"""
        self.logger.info(f"选择城市: {city}")
        self.page.locator(input_locator).click(force=True)
        self.page.locator(input_locator).fill(city)
        try:
            row = self.page.locator(FLIGHT_CITY_SUGGEST_ROW).filter(has_text=city).first
            row.click(timeout=5000)
        except Exception:
            try:
                hot = self.page.locator(FLIGHT_CITY_HOT).filter(has_text=city).first
                hot.click(timeout=3000)
            except Exception:
                self.logger.warning(f"城市「{city}」候选点选失败，继续执行（断言会校验实际行为）")
        # 关闭可能残留的城市下拉，避免遮挡后续操作
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)

    @allure.step("选择出发城市-{from_city}")
    def select_from(self, from_city: str):
        """选择出发城市"""
        self._pick_city(FLIGHT_CITY_FROM, from_city)

    @allure.step("选择到达城市-{to_city}")
    def select_to(self, to_city: str):
        """选择到达城市"""
        self._pick_city(FLIGHT_CITY_TO, to_city)

    @allure.step("设置出发日期-{date}")
    def set_date(self, date: str):
        """设置出发日期，格式 YYYY-MM-DD"""
        self.page.locator(FLIGHT_DATE_INPUT).fill(date)

    def get_date(self) -> str:
        """读取出发日期输入框的值"""
        return self.page.locator(FLIGHT_DATE_INPUT).input_value()

    @allure.step("点击搜索")
    def click_search(self):
        """关闭残留下拉后点击「搜索」；被遮挡时兜底 force 点击"""
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)
        try:
            self.click(FLIGHT_SEARCH_BTN, timeout=8000)
        except Exception:
            self.page.locator(FLIGHT_SEARCH_BTN).click(force=True, timeout=5000)
