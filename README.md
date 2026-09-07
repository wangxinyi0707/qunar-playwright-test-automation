# Qunar Web Test Automation

> 基于 **Playwright + Pytest + POM（Page Object Model）** 的 Web 自动化测试框架，覆盖去哪儿网「首页 → 机票搜索 → 航班列表 → 预订 → 订单查询」核心流程，具备**数据驱动、分层封装、登录态复用、接口 Mock、Allure 报告与日志/截图留证**等工程化能力。

针对去哪儿网这类**强反爬、强登录态、高频改版**的真实业务站点，框架在可维护性、稳定性和可观测性上做了针对性设计，可直接运行、可扩展复用。

---

## 项目亮点

- **POM 四层封装，改动隔离**：定位器（`pages/__init__.py`）→ 页面对象（`pages/`）→ 业务流程（`actions/`）→ 用例（`testcases/`）。页面改版**只需集中修改定位器常量一处**；元素操作、页面行为、业务流程、测试数据各层解耦。
- **数据驱动设计**：用例通过 `pytest.mark.parametrize` 读取 [config](config/) 下的 JSON 数据文件，测试数据与业务逻辑分离，新增场景零代码改动。
- **稳定性工程化**：
  - **Cookie 登录态复用**：一次性手动扫码登录生成 `cookies.json`，注入浏览器 context（Playwright `storage_state`），绕过短信验证码等登录障碍；
  - **接口层 Mock**：针对航班列表/舱位接口的 Bella 反爬加密签名，用真实抓包 schema 拦截 `wbdflightlist` / `wbdflightdetail` 接口（`page.route`），让购票链路在自动化环境稳定渲染；
  - **软断言**：`pytest-assume` 让单条用例的多项校验全部执行完再汇总，避免“断言即停”掩盖更多问题。
- **可观测性**：Allure 功能/故事/步骤标注 + 全流程日志（控制台/文件双输出）+ 用例步骤截图 + 失败保留 Playwright trace，问题可回溯。
- **用例分级**：`smoke`（冒烟）/ `regression`（回归）/ `mock_flight`（Mock 链路）三种标记，支持按需执行；`run.py` 一键运行并生成 Allure 报告。

---

## 覆盖的业务场景

| 模块 | 用例文件 | 数据驱动场景 |
| --- | --- | --- |
| 首页 | [test_home.py](testcases/test_home.py) | 页面加载（标题/Logo/激活导航）+ 顶部导航可见性 |
| 机票搜索 | [test_flight_search.py](testcases/test_flight_search.py) | 正常搜索跳列表 / 同城不跳转 / 过去日期自动纠正 / 不输入跳 fuzzy 页 |
| 机票预订 | [test_flight_book.py](testcases/test_flight_book.py) | 列表 → 展开舱位 → 预订 → 进入订单填写页（Mock 链路）；填单/下单方法完整实现 |
| 订单查询 | [test_order_query.py](testcases/test_order_query.py) | 有订单列表（可按订单号校验）/ 无订单空态文案 |

> 预订/订单查询用例依赖登录态与真实票务会话，详见下文「运行前置」与「已知限制」。

---

## 目录结构（分层职责）

```
qunar-playwright-test-automation/
├── pages/                  # 页面对象层：一个页面一个类，封装“页面上能做什么”
│   ├── __init__.py         # ★ 全部元素定位器集中管理（页面改版只改这里）
│   ├── basepage.py         # 页面基类：点击/输入/读文本/判可见/截图等原子操作
│   ├── page_home.py        # 首页
│   ├── page_login.py       # 统一登录页（手机号/密码/协议勾选）
│   ├── page_flight.py      # 机票搜索页（城市/日期/搜索）
│   ├── page_flight_list.py # 航班列表页（等待渲染/展开舱位/预订）
│   ├── page_booking.py     # 订单填写页（乘机人/联系人/提交/校验提示）
│   └── page_order.py       # 我的机票订单页（列表/空态/订单号校验）
├── actions/                # 业务流程层：组合页面对象方法为“业务动作”
│   ├── home_actions.py     #   打开首页
│   └── flight_actions.py   #   搜索机票 / 直达列表页 / 预订首个航班
├── common/                 # 公共能力
│   └── logger.py           #   统一日志（控制台 + 文件双输出）
├── testcases/              # 用例层：Pytest + Allure + 数据驱动
├── tools/                  # 支撑工具
│   ├── read_json.py        #   读取 config 数据文件
│   ├── save_cookies.py     #   一次性扫码登录生成登录态（cookies.json）
│   └── mock_flight.py      #   航班列表/舱位接口 Mock（真实抓包 schema）
├── config/                 # 数据驱动 JSON：搜索/预订/订单/导航场景数据
├── conftest.py             # 全局 fixture：日志 / 浏览器 context / Cookie 注入 / Mock 开关
├── paths_manager.py        # 路径常量与运行时目录管理
├── pytest.ini              # pytest 配置（base-url / Allure / 标记）
├── run.py                  # 一键跑测 + 生成并打开 Allure 报告
└── requirements.txt
```

**调用链**：`testcases → actions（业务动作）→ pages（页面对象）→ basepage（原子操作）→ Playwright`

---

## 快速开始

### 1. 安装依赖

```bash
cd qunar-playwright-test-automation
python -m venv .venv
# Windows: .venv\Scripts\activate ; Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

框架默认复用**本机已安装的 Chrome**（`conftest.py` 中 `channel="chrome"`），无需下载 Playwright 浏览器内核；若本机没有 Chrome，可去掉该配置后执行 `playwright install chromium`。

### 2. 运行用例

```bash
pytest                # 全量执行（含首页/搜索等游客用例）
pytest -m smoke       # 只跑冒烟用例
pytest -m "not mock_flight"   # 排除 Mock 链路
python run.py         # 一键执行 + 生成并打开 Allure 报告
```

> 报告/日志/截图产物输出到 `reports/`、`logs/`、`images/`，已在 [.gitignore](.gitignore) 中忽略。

### 3. 运行前置（预订 / 订单查询用例）

订单相关用例需要去哪儿登录态：执行一次手动扫码登录，生成 `cookies.json`，conftest 会自动注入：

```bash
python tools/save_cookies.py    # 弹出浏览器 → 扫码登录 → 自动保存登录态
```

---

## 关键机制

### Cookie 登录态复用（绕过短信验证码）

[conftest.py](conftest.py) 中 `browser_context_args` 检测到 `cookies.json` 即通过 Playwright 原生 `storage_state` 注入，用例以已登录身份直接访问订单页等受限页面；登录态过期只需重新运行 [save_cookies.py](tools/save_cookies.py)。

### 接口 Mock（绕过 Bella 反爬）

真实环境中航班列表/舱位接口携带加密签名（Bella 反爬），自动化浏览器拿不到数据。做法：用真实浏览器抓包得到**接口真实 schema**，再通过 `page.route` 拦截 `wbdflightlist` / `wbdflightdetail` 返回桩数据（见 [mock_flight.py](tools/mock_flight.py)）。用例标记 `@pytest.mark.mock_flight` 时，[conftest.py](conftest.py) 的 `page` fixture 自动注册 Mock——桩数据按真实结构构造，页面可正常渲染，预订按钮可真实点击。

### 数据驱动（测试数据与逻辑解耦）

以搜索用例为例（[test_flight_search.py](testcases/test_flight_search.py)）：

```python
@pytest.mark.regression
@pytest.mark.parametrize("data", read_json("flight_search_data.json"), ids=lambda d: d["id"])
def test_search(self, page, data):
    ...
```

[config/flight_search_data.json](config/flight_search_data.json) 中每条数据声明了输入与期望行为（`to_list` / `no_jump` / `corrected` / `fuzzy`），新增场景只加 JSON，不改用例代码。

### 定位器集中管理（应对高频改版）

所有元素定位常量统一收敛在 [pages/__init__.py](pages/__init__.py)，按页面分区并注释含义（如城市候选、舱位展开、预订按钮、乘机人输入框等）；页面对象只引用常量。页面改版时集中定位、一次修改，将改版影响面降到最低。

### 可观测性

- Allure：`@allure.feature / story / title / step` 全链路标注，报告按业务模块组织；
- 日志：`common/logger.py` 输出控制台 + `logs/test.log`，每个操作（点击/输入/截图）留痕；
- 留证：`BasePage.screenshot()` 支持在关键节点/失败时截图到 `images/`；
- Trace：`pytest.ini` 开启 `--tracing=retain-on-failure`，失败用例保留 Playwright 录屏轨迹。

---

## 已知限制（真实环境如实说明）

- 真实下单需要有效乘机人证件与稳定票务会话，**支付环节不做**（行业惯例止步于生成订单）；
- 自动化环境下票务会话 key 过期会让预订页返回“航班售完”，因此 [test_flight_book.py](testcases/test_flight_book.py) 默认以**成功进入订单填写页（URL 含 `book/fill`）**作为断言终点；填单/提交/校验逻辑已完整封装在 [page_booking.py](pages/page_booking.py)，具备真实票务会话的环境可恢复完整下单断言；
- 无订单空态、历史日期纠正等断言覆盖到真实站点常见交互，若站点交互升级，优先调整 [config](config/) 数据或定位器常量即可。

---

## 扩展指南

- 新增页面：在 `pages/` 新增页面对象 + 在 `pages/__init__.py` 登记定位器 → `actions/` 组合业务动作 → `testcases/` 写用例；
- 新增数据场景：在 `config/` 对应 JSON 追加一条即可，无需改用例代码；
- 多环境切换：`pytest.ini` 的 `--base-url` 已接入 `pytest-base-url`，命令行覆盖即可；
- CI 集成：`run.py` / `pytest` 均已输出 Allure 结果（`reports/allure-results`），可直接接入 Jenkins / GitHub Actions 的 allure 插件。
