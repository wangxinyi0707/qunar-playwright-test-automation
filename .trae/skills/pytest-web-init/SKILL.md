---
name: Web-demo
description: 本项目（去哪儿网自动化测试）的测试脚手架说明——分层架构、目录结构、各层职责与约定。用于新建/初始化同类 Playwright + Pytest + PO + Allure + logging 自动化测试项目。
---

# 测试脚手架说明（Playwright + Pytest + PO + Allure + logging）

> 脚手架 = 一套可复用的**项目骨架**（目录结构 + 分层约定 + 基础设施文件），不是某个功能的具体实现。
> 新项目照着这套骨架搭目录、定分层、立约定，再往里填具体的页面/用例代码。

## 一、脚手架解决什么问题

- **定义**：固定的项目骨架（目录 + 分层 + 配置文件 + 基础设施），让任何 Web 自动化测试项目都能快速起步、结构统一。
- **价值**：职责清晰、易维护、好交接、方便多人协作（也是面试展示点）。
- **技术栈**：Playwright（同步 API）+ pytest-playwright + Pytest + Page Object 三层 + 数据驱动 + Allure + logging + Cookie 登录态复用。

## 二、目录结构（骨架全貌）

```
项目根/
├── actions/          # 业务动作层：组合页面对象方法，完成一个业务动作
├── common/           # 底层封装：logger（日志）
├── pages/            # 页面对象层（PO）
│   ├── basepage.py   #   BasePage 基类：通用操作（点击/输入/截图…）
│   ├── page_xxx.py   #   各被测页面对象
│   └── __init__.py   #   所有元素定位器集中管理
├── config/           # 测试数据（json，数据驱动）
├── testcases/        # 测试用例
├── tools/            # 纯工具：读 json / cookie 处理
├── conftest.py       # 全局 fixture：日志初始化、浏览器 context 配置
├── paths_manager.py  # 项目路径常量
├── pytest.ini        # pytest 配置（alluredir、tracing 等）
├── run.py            # 一键跑测试 + 生成 allure 报告
└── requirements.txt  # 依赖清单
```

## 三、分层职责（脚手架的灵魂）

共 **四层** + **两套基础设施**：

### 1. 底层封装层（`common/` + `pages/basepage.py`）
- `common/logger.py`：全项目统一日志入口。
- `pages/basepage.py`：`BasePage` 基类，封装**所有页面共用**的原子操作——点击、输入、读文本、判可见、截图等；持有 `page` 和 `logger`。
- 职责：只提供「怎么操作元素」的通用能力，不关心具体业务。

### 2. 页面对象层（`pages/`）
- 每个被测页面一个 `page_xxx.py`，继承 `BasePage`。
- 只描述「这个页面有哪些元素、能做什么」，返回操作结果/状态，不做业务编排。
- `pages/__init__.py`：**所有元素定位器（选择器字符串）集中管理**——页面改版只改这一处。

### 3. 业务动作层（`actions/`）
- 组合多个页面对象方法，完成一个**有业务含义**的动作（如「登录」「填写搜索表单」）。
- 测试用例只调动作层，不直接碰页面对象细节。

### 4. 测试用例层（`testcases/`）
- 用 `page` fixture + 数据驱动 + 软断言写用例。
- 只做「断言结果对不对」，不写操作细节。

### 5. 数据层（`config/`）
- 测试数据放 json，用 `@pytest.mark.parametrize` 参数化，实现**数据驱动**（同一套用例跑多组数据）。

### 6. 工具层（`tools/`）
- 与业务无关的纯工具：读 json、cookie 读写等。

### 7. 基础设施文件
| 文件 | 职责 |
|---|---|
| `conftest.py` | 全局 fixture：日志初始化、浏览器 context 配置（`page` fixture 由 pytest-playwright 自动提供） |
| `paths_manager.py` | 项目路径常量（json 路径、截图路径等） |
| `pytest.ini` | pytest 配置（alluredir、tracing、testpaths、命名规则） |
| `run.py` | 一键跑测试 + 生成 allure 报告 |
| `requirements.txt` | 依赖清单 |

## 四、约定与规范

- **API 风格**：同步（普通 `def`，无 async/await，不装 pytest-asyncio），规避事件循环冲突。
- **定位器**：全部用字符串（CSS / XPath），集中放 `pages/__init__.py`。
- **断言**：`pytest.assume` 软断言——一次跑完所有校验点，不因第一个失败就中断。
- **失败留证**：失败时 `page_obj.screenshot()` 截图；`pytest.ini` 默认 `--tracing=retain-on-failure` 自动留 trace。
- **登录态**：Cookie 复用（`save_cookies.py` 一次性手动登录生成，测试注入 Cookie 绕过短信验证码）。
- **数据驱动**：`config/*.json` + `@pytest.mark.parametrize`。
- **命名**：测试文件 `test_*.py`、测试类 `Test*`、测试方法 `test_*`。

## 五、从零初始化一个新项目

```bash
# 1. 建虚拟环境并激活（Windows）
python -m venv .venv
.venv\Scripts\activate

# 2. 装依赖
pip install playwright pytest-playwright pytest pytest-assume pytest-xdist allure-pytest

# 3. 装浏览器内核（国内网络慢时加镜像）
playwright install chromium

# 4. 建目录骨架
mkdir -p actions common pages config testcases tools logs images
```

> 目录骨架建好后，按「第三节」的职责，依次补上 `conftest.py`、`paths_manager.py`、`pytest.ini`、`run.py`、`requirements.txt` 等基础设施文件，以及 `common/logger.py`、`pages/basepage.py` 两个底层封装，脚手架即就绪。

## 六、脚手架怎么用（与其他技能衔接）

- 搭骨架、定分层 → 本技能（`scaffold-project`）
- 往里填具体页面/用例代码 → [[new-test]]
- 跑测试、看报告 → [[run-tests]]
- 失败排错 → [[debug-failure]]
