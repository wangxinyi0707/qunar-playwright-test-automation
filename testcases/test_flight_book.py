"""用例2：机票购买（需登录态）

当前环境限制：预订页航班数据由服务端按票务 key 渲染（自动化下票务会话过期即返回「航班售完」），
表单填写/下单断言需真实票务会话，故本用例验证到「进入订单填写页」为止——
真实链路：列表渲染 → 舱位展开 → 预订按钮 → 新开预订页（URL 含 book/fill）。
真实环境（非沙箱）可恢复：fill_passenger/fill_contact/submit_order + 订单断言。
"""
import allure
import pytest
from pytest_assume.plugin import assume

from actions.flight_actions import book_first_flight, open_flight_list
from tools.read_json import read_json


@allure.feature("机票购买")
@pytest.mark.mock_flight
class TestFlightBook:
    """列表 → 舱位 → 预订 → 进入订单填写页"""

    @allure.story("预订流程")
    @allure.title("机票购买-{data[id]}")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", read_json("book_data.json"), ids=lambda d: d["id"])
    def test_book(self, page, data):
        # 1. 打开航班列表（接口 Mock，规避反爬空态）
        lst = open_flight_list(page, data["from_code"], data["to_code"], data["date"], data["from"], data["to"])
        assume(lst.wait_for_flights(), "航班列表应出现（接口 Mock 生效）")

        # 2. 展开舱位 → 点击预订 → 进入订单填写页（新开标签页）
        book = book_first_flight(page)
        assume(
            book.is_on_booking_page(),
            f"应进入订单填写页（URL 含 book/fill），实际: {book.page.url[:150]}",
        )
