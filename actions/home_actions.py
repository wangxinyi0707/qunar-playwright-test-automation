"""首页业务动作层：组合页面对象方法，完成一个有业务含义的动作"""
from pages.page_home import HomePage


def open_home(page, base_url: str) -> HomePage:
    """业务动作：打开去哪儿网首页，返回首页对象供断言"""
    home = HomePage(page)
    home.open(base_url)
    return home
