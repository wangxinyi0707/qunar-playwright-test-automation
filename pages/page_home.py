"""去哪儿网首页页面对象：只描述「首页有哪些元素、能做什么」，不做业务编排"""
from pages import HOME_LOGO, HOME_NAV_ACTIVE, HOME_NAV_BY_TEXT
from pages.basepage import BasePage


class HomePage(BasePage):
    def is_logo_visible(self) -> bool:
        """Logo 是否可见"""
        return self.is_visible(HOME_LOGO)

    def get_active_nav(self) -> str:
        """获取当前激活的顶部导航文字"""
        return self.get_text(HOME_NAV_ACTIVE)

    def has_nav(self, text: str) -> bool:
        """顶部导航是否包含指定文字项"""
        return self.is_visible(HOME_NAV_BY_TEXT.format(text=text))
