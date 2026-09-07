"""机票业务流程动作层：组合页面对象方法，完成有业务含义的动作"""
from urllib.parse import urlencode

from pages.page_booking import BookingPage
from pages.page_flight import FlightSearchPage
from pages.page_flight_list import FlightListPage

# 航班列表页地址（oneway_list.htm）
FLIGHT_LIST_URL = "https://flight.qunar.com/site/oneway_list.htm"


def search_flight(page, from_city: str, to_city: str, date: str) -> FlightListPage:
    """业务动作：在搜索页搜索机票（真实流程，用于验证搜索跳转）"""
    search = FlightSearchPage(page)
    search.open_flight()
    search.select_from(from_city)
    search.select_to(to_city)
    search.set_date(date)
    search.click_search()
    return FlightListPage(page)


def open_flight_list(page, from_code: str, to_code: str, date: str,
                     from_city: str = "", to_city: str = "") -> FlightListPage:
    """业务动作：直接打开航班列表页（配合接口 Mock 稳定渲染，规避表单提交导航挂起）"""
    params = {
        "searchDepartureAirport": from_city or "",
        "searchArrivalAirport": to_city or "",
        "searchDepartureTime": date,
        "searchArrivalTime": "",
        "nextNDays": 0,
        "startSearch": True,
        "fromCode": from_code,
        "toCode": to_code,
        "from": "flight_dom_search",
    }
    page.goto(f"{FLIGHT_LIST_URL}?{urlencode(params)}", timeout=30000, wait_until="domcontentloaded")
    return FlightListPage(page)


def book_first_flight(page) -> BookingPage:
    """业务动作：预订列表页第一个航班（通常新开标签页），等待进入订单填写页后返回

    注意：预订页在自动化环境下可能加载缓慢/挂起，这里全部用短超时轮询，避免被挂死。
    """
    lst = FlightListPage(page)
    lst.expand_first_price()
    try:
        with page.expect_popup(timeout=15000) as popup_info:
            lst.click_book()
        book_page = popup_info.value
    except Exception:
        # 兜底：预订在本页打开而非新标签页
        book_page = page
    book_page.set_default_timeout(8000)
    # 轮询等待进入订单填写页（不依赖 load_state，防挂起）
    for _ in range(10):
        if "book/fill" in book_page.url:
            break
        book_page.wait_for_timeout(1000)
    book_page.wait_for_timeout(3000)
    return BookingPage(book_page)
