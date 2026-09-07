"""BasePage 基类：封装所有页面共用的原子操作（点击/输入/读文本/判可见/截图等）

只提供「怎么操作元素」的通用能力，不关心具体业务。
"""
import allure
from playwright.sync_api import Page

from common.logger import get_logger
from paths_manager import IMAGES_DIR


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()

    def open(self, url: str):
        """打开指定 URL"""
        self.logger.info(f"打开页面: {url}")
        self.page.goto(url)

    def click(self, locator: str, timeout: int = 10000):
        """点击元素"""
        self.logger.info(f"点击元素: {locator}")
        self.page.click(locator, timeout=timeout)

    def fill(self, locator: str, text: str):
        """输入文本"""
        self.logger.info(f"输入文本: {locator} = {text}")
        self.page.fill(locator, text)

    def check(self, locator: str):
        """勾选复选框"""
        self.logger.info(f"勾选复选框: {locator}")
        self.page.check(locator)

    def get_text(self, locator: str) -> str:
        """读取元素文本"""
        text = self.page.text_content(locator)
        self.logger.info(f"读取文本: {locator} = {text}")
        return text

    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """判断元素是否可见"""
        try:
            self.page.wait_for_selector(locator, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    @allure.step("截图留证")
    def screenshot(self, name: str = "screenshot") -> str:
        """失败时调用，截图留证"""
        path = IMAGES_DIR / f"{name}.png"
        self.page.screenshot(path=str(path))
        self.logger.info(f"截图保存: {path}")
        return str(path)
