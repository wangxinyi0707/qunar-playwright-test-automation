"""用例3：订单查询（需登录态）

前置：conftest 注入 Cookie 登录态。has_order 场景可把用例2生成的订单号填入 order_data.json 的 order_no。
"""
import allure
import pytest
from pytest_assume.plugin import assume

from pages.page_order import OrderPage
from tools.read_json import read_json


@allure.feature("订单查询")
class TestOrderQuery:
    """进入我的机票订单页 → 校验订单列表/空态"""

    @allure.story("订单列表")
    @allure.title("订单查询-{data[id]}")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", read_json("order_data.json"), ids=lambda d: d["id"])
    def test_query(self, page, data):
        order = OrderPage(page)
        order.open_orders()
        page.wait_for_timeout(3000)
        assume("flight.order.qunar.com" in page.url, f"应在我的机票订单页，实际: {page.url[:120]}")

        if data["expect_empty"]:
            # no_order：账号下无订单（或筛选无结果）→ 出现空态提示
            assume(not order.has_order_list(3000) or order.is_empty(), "无订单时应出现空态提示")
            if order.is_empty():
                body = page.evaluate("document.body ? document.body.innerText : ''")
                assume("没有符合条件" in body, "空态文案应为「没有符合条件的订单，请尝试其他搜索条件」")
        else:
            # has_order：订单列表出现，并可查到指定订单号
            assume(order.has_order_list(), "订单列表应出现")
            if data["order_no"]:
                assume(order.has_order(data["order_no"]), f"应能查到订单号 {data['order_no']}")
