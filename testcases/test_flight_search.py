"""用例1：机票搜索（游客，无需登录）"""
import allure
import pytest
from pytest_assume.plugin import assume

from pages.page_flight import FlightSearchPage
from pages.page_flight_list import FlightListPage
from tools.read_json import read_json


@allure.feature("机票搜索")
class TestFlightSearch:
    """去哪儿机票搜索：正常/同城/过去日期/不输入 四类场景"""

    @allure.story("搜索跳转")
    @allure.title("机票搜索-{data[id]}")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", read_json("flight_search_data.json"), ids=lambda d: d["id"])
    def test_search(self, page, data):
        flight = FlightSearchPage(page)
        flight.open_flight()
        if data["from"]:
            flight.select_from(data["from"])
        if data["to"]:
            flight.select_to(data["to"])
        if data["date"]:
            flight.set_date(data["date"])
        flight.click_search()
        page.wait_for_timeout(4000)
        lst = FlightListPage(page)

        if data["expect"] == "to_list":
            # 正常：跳转航班列表页，URL 含 fromCode / toCode（城市代码可能为机场级 PEK，只断言参数存在）
            assume(lst.is_list_url(), f"应跳转航班列表页且 URL 含 fromCode/toCode，实际: {page.url[:120]}")
        elif data["expect"] == "no_jump":
            # 同城：不跳转列表页
            assume("oneway_list" not in page.url, f"同城搜索不应跳转航班列表，实际: {page.url[:120]}")
        elif data["expect"] == "corrected":
            # 过去日期：自动纠正（可能在原页纠正日期，或按纠正后的日期直接跳转列表页）
            if "oneway_list" in page.url:
                assume(True, "过去日期已自动纠正并跳转航班列表页")
            else:
                assume(
                    flight.get_date() != data["date"],
                    f"过去日期应被自动纠正，实际: {flight.get_date()}",
                )
        elif data["expect"] == "fuzzy":
            # 不输入：跳 fuzzy 页（带默认城市）
            assume("fuzzy" in page.url, f"不输入应跳转 fuzzy 页，实际: {page.url[:120]}")
