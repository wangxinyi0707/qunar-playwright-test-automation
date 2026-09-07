"""首页用例：数据驱动 + 软断言"""
import allure
import pytest
from pytest_assume.plugin import assume

from actions.home_actions import open_home
from tools.read_json import read_json


@allure.feature("首页")
class TestHome:
    """去哪儿网首页相关用例"""

    @allure.story("页面加载")
    @allure.title("验证首页可正常打开")
    @pytest.mark.smoke
    def test_home_load(self, page, base_url):
        home = open_home(page, base_url)
        assume("去哪儿" in home.title(), f"首页标题应包含「去哪儿」，实际: {home.title()}")
        assume(home.is_logo_visible(), "首页 Logo 应可见")
        assume(home.get_active_nav() == "首页", f"激活导航应为「首页」，实际: {home.get_active_nav()}")

    @allure.story("顶部导航")
    @allure.title("顶部导航项-{nav}")
    @pytest.mark.regression
    @pytest.mark.parametrize("nav", [d["nav"] for d in read_json("home_nav_data.json")])
    def test_nav_item_visible(self, page, base_url, nav):
        home = open_home(page, base_url)
        assume(home.has_nav(nav), f"顶部导航应包含「{nav}」")
