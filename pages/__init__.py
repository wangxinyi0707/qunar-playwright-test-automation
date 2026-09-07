"""所有元素定位器集中管理——页面改版只改这一处"""
# ================= 首页（page_home.py） =================
# 顶部 Logo 图片
HOME_LOGO = ".logo img"
# 顶部导航项
HOME_NAV_ITEM = ".header-pc .nav-labe"
# 当前激活的导航项
HOME_NAV_ACTIVE = ".header-pc .nav-labe.actived"
# 按文字匹配的导航项模板
HOME_NAV_BY_TEXT = ".header-pc .nav-labe:has-text('{text}')"

# ================= 登录页（page_login.py） =================
# 统一登录页基础地址（ret 参数为登录成功后的跳转地址）
LOGIN_BASE_URL = "https://user.qunar.com/passport/login.jsp"

# 登录方式 Tab
LOGIN_TAB_PHONE = ".phoneTab"          # 手机号登录/注册（默认激活）
LOGIN_TAB_PASSWORD = ".passwordTab"    # 密码登录

# 手机号登录模式
LOGIN_COUNTRY_CODE_INPUT = "input[placeholder='请输入国家区号']"
LOGIN_PHONE_INPUT = "#telphone"
LOGIN_CODE_INPUT = "#codenum"
LOGIN_GET_CODE_BTN = "span.codeButton"           # 获取验证码
LOGIN_PHONE_SUBMIT = "span:text-is('登录/注册')"   # 提交登录/注册

# 密码登录模式
LOGIN_USERNAME_INPUT = "#username"
LOGIN_PASSWORD_INPUT = "#password"
LOGIN_PASSWORD_SUBMIT = "span:text-is('登录')"    # 提交登录

# 协议勾选
LOGIN_AGREEMENT_CHECKBOX = "#agreement"

# ================= 机票搜索页（page_flight.py） =================
FLIGHT_URL = "https://flight.qunar.com/"
FLIGHT_FORM = "#dfsForm"                                            # 国内机票搜索表单
FLIGHT_CITY_FROM = "#dfsForm input[name='fromCity']"                # 出发城市输入框
FLIGHT_CITY_TO = "#dfsForm input[name='toCity']"                    # 到达城市输入框
FLIGHT_CITY_SUGGEST_ROW = "#dfsForm div.js-suggestcontainer table tr"  # 城市候选行
FLIGHT_CITY_HOT = "#dfsForm a.js-hotcitylist"                       # 热门城市链接
FLIGHT_DATE_INPUT = "#dfsForm #fromDate"                            # 出发日期输入框
FLIGHT_SEARCH_BTN = "#dfsForm button.btn_search"                    # 搜索按钮

# ================= 航班列表页（page_flight_list.py） =================
FLIGHT_LIST_CONTAINER = "div.m-airfly-lst"                          # 航班列表容器
FLIGHT_LIST_ROW = "div.m-airfly-lst > div.b-airfly"                 # 航班行
FLIGHT_PRICE = "div.col-price > p.prc"                              # 价格（点击展开舱位）
FLIGHT_BOOK_BTN = "button.btn-book"                                 # 预订按钮（展开舱位后出现）
FLIGHT_LIST_EMPTY = "div.m-load > div.e-txt"                        # 空态提示

# ================= 订单填写/预订页（page_booking.py） =================
BOOKING_PASSENGER_NAME = "input.js-passenger-name"                  # 乘机人姓名
BOOKING_PASSENGER_CERT = "input.js-cert-number"                     # 乘机人证件号
BOOKING_ADD_PASSENGER = "button.js-addPassenger"                    # 添加乘机人
BOOKING_CONTACT_NAME = "input.contact-name"                         # 联系人姓名
BOOKING_CONTACT_PHONE = "input.js-contact-phone"                    # 联系人手机号
BOOKING_SUBMIT = "div.darkblue-button.button-input"                 # 提交订单

# ================= 订单列表页（page_order.py） =================
ORDER_LIST_URL = "http://flight.order.qunar.com/flight"             # 我的机票订单（需登录）
ORDER_LIST_CONTAINER = "div#order-list"                             # 订单列表容器
ORDER_LIST_EMPTY = "div.order-bought > p.no-list"                   # 空态提示
