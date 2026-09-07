"""全局 fixture：日志初始化、浏览器 context 配置"""
import pytest

from common.logger import get_logger
from paths_manager import COOKIE_FILE


@pytest.fixture(scope="session", autouse=True)
def init_logger():
    """初始化全项目统一日志"""
    get_logger()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """浏览器启动参数：复用系统安装的 Chrome，无需 playwright install 下载浏览器内核"""
    args = dict(browser_type_launch_args)
    args["channel"] = "chrome"
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """浏览器 context 配置：若存在已保存的 Cookie 登录态文件则注入，绕过短信验证码等登录障碍"""
    args = dict(browser_context_args)
    if COOKIE_FILE.exists():
        # storage_state 直接指向 cookie 文件（Playwright 原生支持）
        args["storage_state"] = str(COOKIE_FILE)
    return args


@pytest.fixture(scope="function")
def page(page, request):
    """页面 fixture：标记了 @pytest.mark.mock_flight 的用例自动 Mock 航班数据接口（规避反爬空态）"""
    if request.node.get_closest_marker("mock_flight"):
        from tools.mock_flight import register_flight_mock

        register_flight_mock(page)
    yield page
