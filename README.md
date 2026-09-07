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
