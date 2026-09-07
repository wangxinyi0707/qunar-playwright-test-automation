# 基于 Playwright 的 Web 自动化测试框架

> 基于 **Playwright + Pytest + POM（Page Object Model）** 构建的 Web 自动化测试框架，覆盖去哪儿网机票预订核心流程的自动化测试，并引入 **AI Agent 辅助元素定位与脚本修复**。

## 项目介绍

本框架面向去哪儿网真实业务站点，采用 **页面对象模型** 分层设计，完成「首页 → 机票搜索 → 航班列表 → 机票预订 → 订单查询」核心流程的自动化测试；同时沉淀了开发期使用的 AI Agent 技能与 Playwright CLI 工具，辅助页面元素定位策略优化与脚本异常修复，兼顾框架的可维护性与可观测性。

## 主要工作与核心亮点

1. **POM 分层封装**：基于 POM 模式搭建自动化测试框架，分层封装基础操作（`pages/basepage.py`）、页面对象（`pages/`）与业务流程（`actions/`）；全部元素定位器集中管理，页面改版一处维护、影响面最小；
2. **AI Agent 辅助定位与修复**：利用 AI Agent 解析页面 DOM、优化元素定位策略并辅助分析与修复脚本异常——相关能力沉淀为项目内可复用的 AI 技能（`.trae/skills/`：web-demo-scaffold 脚手架生成、pytest-web-init 测试脚手架规范）与 Playwright CLI 快捷工具（`.playwright-cli/`）；
3. **Pytest + Allure 报告与运行日志**：使用 Pytest 组织与管理测试用例，结合 Allure 生成结构化测试报告（feature / story / step 全链路标注），全程记录运行日志并支持步骤截图留证；
4. **数据驱动设计**：测试数据以 JSON 存放于 `config/`，通过参数化注入用例，实现**测试数据与业务逻辑解耦**，新增场景只需追加数据、无需改动用例代码。

## 业务覆盖

| 业务流程 | 页面对象 | 覆盖场景 |
| --- | --- | --- |
| 首页 | `page_home.py` | 页面加载、顶部导航可见性 |
| 机票搜索 | `page_flight.py` | 正常搜索、同城搜索、过去日期纠正、空输入跳转 |
| 航班列表 | `page_flight_list.py` | 列表渲染、舱位展开、预订入口 |
| 机票预订 | `page_booking.py` | 乘机人/联系人填写、订单提交、表单校验提示 |
| 订单查询 | `page_order.py` | 订单列表校验、空态处理 |

## 技术栈

| 类别 | 技术 |
| --- | --- |
| UI 自动化 | Playwright（同步 API，复用系统 Chrome） |
| 测试框架 | Pytest · pytest-playwright · pytest-base-url · pytest-assume |
| 分层设计 | POM（定位器层 / 页面对象 / 业务动作 / 用例层） |
| 报告与日志 | Allure · logging（控制台 + 文件双输出）· 失败截图与 Trace |
| 数据驱动 | config/JSON 参数化 |
| AI 辅助 | Trae AI Agent 技能（.trae/skills）· Playwright CLI 工具（.playwright-cli） |

## 目录结构

```
├── pages/                  # 页面对象层（页面对象 + 元素定位器集中管理）
│   ├── __init__.py         # 全部元素定位器常量
│   ├── basepage.py         # 页面基类：点击/输入/读取/截图等原子操作
│   └── page_*.py           # 首页 / 登录 / 机票搜索 / 航班列表 / 预订 / 订单页
├── actions/                # 业务流程层：组合页面对象为业务动作
├── common/                 # 公共能力：统一日志（logger）
├── testcases/              # 用例层：Pytest + Allure + 数据驱动
├── tools/                  # 工具：JSON 读取、Cookie 登录态、浏览器操作辅助
├── config/                 # 数据驱动测试数据（JSON）
├── conftest.py             # 全局 fixture：浏览器 context、登录态注入
├── .trae/skills/           # AI Agent 技能（脚手架生成 / 测试脚手架规范）
├── .playwright-cli/        # Playwright CLI 快捷工具
├── paths_manager.py        # 项目路径常量
├── pytest.ini              # pytest 配置
├── run.py                  # 一键运行并生成 Allure 报告
└── requirements.txt        # 依赖清单
```

## 快速开始

```bash
pip install -r requirements.txt   # 复用本机 Chrome，无需 playwright install
pytest                             # 执行全部用例
pytest -m smoke                    # 按标记执行（smoke / regression）
python run.py                      # 一键跑测并生成/打开 Allure 报告
```

## 注意事项

- **登录态安全**：订单等需登录场景由 `tools/save_cookies.py` 一次性扫码生成 `cookies.json` 并由 `conftest.py` 自动注入浏览器 context；Cookie 文件已加入 `.gitignore`，账号凭证不入库、不共享，团队成员各自生成即可。
- **环境适配成本低**：框架默认复用本机已安装的 Chrome（`channel="chrome"`），无需 `playwright install` 下载浏览器内核；CI 或纯净环境可一键切换为标准浏览器安装模式。
- **改版维护成本收敛**：页面元素定位器统一登记在 `pages/__init__.py`，页面对象只表达“页面上能做什么”，业务流程在 `actions/` 层组合——页面改版时只需更新定位器常量，业务与用例层完全不动，将维护影响面收敛到单点。
- **数据驱动、零代码加场景**：新增测试场景只需在 `config/` 对应 JSON 中追加一条数据并声明期望行为，用例自动参数化执行，业务逻辑无需改动。
- **失败可追溯**：`pytest.ini` 默认收集 Allure 结果到 `reports/` 并保留失败 Trace，叠加运行日志与步骤截图，定位失败环节一目了然，便于 CI 归档与回归分析。
- **用例分级、按需执行**：`smoke` / `regression` 标记支持分层运行（如 `pytest -m smoke`），日常冒烟与发版前全量回归可灵活切换，平衡执行时长与覆盖度。
