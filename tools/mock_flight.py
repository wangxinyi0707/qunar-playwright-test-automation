"""航班数据接口 Mock（wbdflightlist / wbdflightdetail）

背景：真实环境航班列表/舱位接口带 Bella 反爬令牌（加密签名），自动化浏览器无法通过校验，
服务端返回 code=-1 空列表。为让购票用例稳定跑通，拦截这两个接口并返回**真实 schema** 的桩数据。

说明：桩数据字段均来自真实接口抓包（子代理在真实浏览器会话中捕获），页面可正常渲染。
"""
import json

from playwright.sync_api import Route

# ---------------- wbdflightlist（航班列表） ----------------
FLIGHT_LIST_MOCK = {
    "ret": True,
    "code": 0,
    "msg": "请求成功",
    "data": {
        "allFilter": [],
        "min_flight": {
            "all": {"price": 272, "tag": "CZA1", "domain": "MOCK", "code": "CZ8899"},
            "list": {"price": 272, "tag": "CZA1", "domain": "MOCK", "code": "CZ8899"},
            "listMore": {"code": "CZ8899", "price": 272},
        },
        "flights": [
            {
                "binfo": {
                    "airCode": "CZ8899", "arrAirport": "虹桥机场", "arrAirportCode": "SHA",
                    "arrDate": "2026-08-30", "stops": False, "stopTime": "", "stopCitys": [],
                    "stopAirports": [], "arrTerminal": "T2", "arrTime": "10:10", "cabin": "Z",
                    "codeShare": False, "crossDay": 0, "crossDayDesc": "", "date": "2026-08-30",
                    "depAirport": "北京大兴机场", "depAirportCode": "PKX", "depDate": "2026-08-30",
                    "depTerminal": "", "depTime": "08:00", "distance": 1227, "flightTime": "2h10m",
                    "fullName": "南方航空", "isInter": False, "lateTime": "-11",
                    "mainCarrierShortName": "", "meal": True, "mealDesc": "有餐食",
                    "name": "南方航空", "planeFullType": "空客320(中)", "planeType": "327",
                    "shortCarrier": "CZ", "shortName": "南航", "tof": "70", "zhiji": True,
                    "piaoShao": False, "piaoShaoDesc": "", "pTrip": False, "pTripNote": "",
                    "depAirportHighlight": True, "arrAirportHighlight": False,
                },
                "minPrice": 272, "minbfPrice": 0, "code": "CZ8899", "extparams": "{}",
                "flightType": "list", "crossDayDesc": "", "transCity": "", "transTime": 0,
                "discountStr": "2.6折", "priceLabel": [],
            }
        ],
        "total": 1,
        "geographyInfo": {
            "depCity": {
                "cityZh": "北京", "cityEn": "beijing", "city": "PEK",
                "airportInfoList": [
                    {"airportFullName": "北京首都国际机场", "airportShortName": "首都机场", "airport": "PEK"},
                    {"airportFullName": "北京大兴国际机场", "airportShortName": "北京大兴机场", "airport": "PKX"},
                ],
            },
            "arrCity": {
                "cityZh": "上海", "cityEn": "shanghai", "city": "SHA",
                "airportInfoList": [
                    {"airportFullName": "上海虹桥国际机场", "airportShortName": "虹桥机场", "airport": "SHA"},
                    {"airportFullName": "上海浦东国际机场", "airportShortName": "浦东机场", "airport": "PVG"},
                ],
            },
        },
    },
}

# ---------------- wbdflightdetail（舱位/预订详情） ----------------
# 舱位对象字段与真实抓包一致；bookingUrl 为可点的预订地址（新开标签页）
# 注意真实结构：data.routes[0].vendors 是数组套数组（vendors[0] 为经济舱列表，vendors[1] 为公务舱列表）
_CABIN = {
    "bookingName": "预订",
    # 使用真实抓包得到的预订地址（含真实航班 key），预订页才能查到航班数据并渲染表单
    "bookingUrl": "//qnf.trade.qunar.com/ns/book/fill?p=f_domestic_uniform_booking_CZ8899_CZA1_c25b5650-c751-4f51-9a03-e3e70d3c82f5",
    "price": 338,
    "name": "超值特惠",
    "cname": "中国南方航空股份有限公司",
    "IATA": "00001704",
    "cd": "",
    "fxPrice": 0,
    "insurePrice": 0,
    "logo": "",
    "airways": "南方航空",
    "airwaysShortName": "",
    "airwaysFullName": "中国南方航空公司",
    "discount": "2.6",
    "carrier": "CZ",
    "isSelf": "",
    "isApply": "",
    "cabin": "Z",
    "cabinTypeName": "经济舱2.6折",
    "cabinTypeNote": [],
    "packageProduct": [],
    "labels": [],
    "priceLables": [],
    "pointForCommon2": [],
}

_CABIN_BUSINESS = {
    **_CABIN,
    "price": 1508,
    "name": "南航商务舱",
    "discount": "3.5",
    "cabin": "I",
    "cabinTypeName": "公务舱3.5折",
    "bookingUrl": "//qnf.trade.qunar.com/ns/book/fill?p=f_domestic_uniform_booking_CZ8899_TYB1_c25b5650-c751-4f51-9a03-e3e70d3c82f5",
}

FLIGHT_DETAIL_MOCK = {
    "ret": True,
    "code": 0,
    "msg": "请求成功",
    "data": {
        "pointForPv2": [],
        "routes": [
            {
                "flightType": 81,
                "fInfos": [
                    {
                        "goInfos": [
                            {
                                "airlineCode": "CZ", "airlineName": "南方航空", "airlineShortName": "南航",
                                "airlineFullName": "中国南方航空公司",
                                "arrAirportFull": "上海虹桥国际机场", "arrAirport": "虹桥机场", "arrApCode": "SHA",
                                "arrCity": "", "arrDate": "2026-08-30", "crossDay": 0, "crossDayDesc": "",
                                "arrTerminal": "T2", "arrTime": "10:10", "correct": "97%", "correctDesc": "准点率97%",
                                "depAirportFull": "北京大兴国际机场", "depAirport": "北京大兴机场", "depApCode": "PKX",
                                "depCity": "", "depDate": "2026-08-30", "depTerminal": "", "depTime": "08:00",
                                "distance": 1227, "flightNo": "CZ8899", "flightTime": "2时10分",
                                "isShareFlight": False, "meal": True, "mealDesc": "点心", "shareFlight": False,
                                "planeType": "空客320(中)", "fuelTax": "以下价格不包括机建燃油费",
                                "stop": False, "stopCitys": [], "stopAirports": [], "zhiji": True, "self": False,
                            }
                        ]
                    }
                ],
                "lab": ["全部", "头等/商务舱"],
                "vendors": [
                    [_CABIN],
                    [_CABIN_BUSINESS],
                ],
            }
        ],
    },
}


def mock_wbdflightlist(route: Route):
    """拦截航班列表接口"""
    route.fulfill(
        status=200,
        content_type="application/json; charset=utf-8",
        body=json.dumps(FLIGHT_LIST_MOCK, ensure_ascii=False),
    )


def mock_wbdflightdetail(route: Route):
    """拦截舱位/预订详情接口"""
    route.fulfill(
        status=200,
        content_type="application/json; charset=utf-8",
        body=json.dumps(FLIGHT_DETAIL_MOCK, ensure_ascii=False),
    )


def register_flight_mock(page):
    """在页面上注册航班数据接口 Mock（供购票用例使用）"""
    page.route("**/touch/api/domestic/wbdflightlist", mock_wbdflightlist)
    page.route("**/touch/api/domestic/wbdflightdetail", mock_wbdflightdetail)
