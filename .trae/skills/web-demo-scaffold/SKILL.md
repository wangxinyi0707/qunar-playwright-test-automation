---
name: "web-demo-scaffold"
description: "生成基于 Playwright + Pytest 的 Web 自动化测试脚手架到 web-demo 目录。当用户要求生成/搭建 web 自动化测试项目脚手架、创建 web-demo 结构或从零开始搭建 web 测试项目时调用。"
---

# Web 自动化测试脚手架生成器（web-demo）

## 目标

在项目根目录下生成一个完整、可直接运行的 `web-demo/` 自动化测试脚手架，技术栈为 **Playwright + Pytest + Page Object Model（POM）**。

## 生成结构

```
web-demo/
├── requirements.txt        # 依赖清单
├── pytest.ini              # pytest 配置（含 addopts、markers、超时等）
├── conftest.py             # 全局 fixture（browser、page、base_url 等）
├── config/
│   ├── __init__.py
│   └── settings.py         # 全局配置（BASE_URL、超时时间、浏览器类型等）
├── pages/
│   ├── __init__.py
│   └── base_page.py        # 页面基类（封装常用操作：打开、点击、输入、断言等）
├── tests/
│   ├── __init__.py
│   └── test_home.py        # 示例测试用例（含 allure 步骤与断言）
└── utils/
    ├── __init__.py
    └── logger.py           # 日志工具（可选，若脚手架不需要可省略）
```

## 生成步骤

1. **创建目录结构**：按上述结构在项目根目录下创建 `web-demo/` 及所有子目录。
2. **写入文件内容**：按下方「文件内容模板」逐个写入，所有代码注释使用中文。
3. **验证可运行性**：确保 `conftest.py` 的 fixture 与 `pytest.ini` 配置匹配，用例能通过 `pytest web-demo` 或 `pytest web-demo/tests` 收集执行。

## 文件内容模板

### requirements.txt

```
playwright>=1.40.0
pytest>=7.0.0
pytest-base-url>=2.0.0
pytest-playwright>=0.4.0
allure-pytest>=2.13.0
```

### pytest.ini

```ini
[pytest]
addopts = -v -s --base-url=https://www.qunar.com --headed
testpaths = tests
markers =
    smoke: 冒烟测试
    regression: 回归测试
timeout = 30000
```

### conftest.py

```python
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context():
    """启动浏览器，使用系统 Chrome，避免重复下载浏览器内核"""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context(locale="zh-CN")
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """每个用例独立的新页面"""
    page = browser_context.new_page()
    page.set_default_timeout(30000)
    yield page
    page.close()
```

### config/settings.py

```python
"""全局配置"""

BASE_URL = "https://www.qunar.com"
BROWSER_TYPE = "chromium"
HEADLESS = False
TIMEOUT = 30000
```

### pages/base_page.py

```python
"""页面基类，封装常用操作"""


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url):
        """打开指定 URL"""
        self.page.goto(url)

    def click(self, locator):
        """点击元素"""
        self.page.click(locator)

    def fill(self, locator, text):
        """输入文本"""
        self.page.fill(locator, text)

    def get_text(self, locator):
        """获取元素文本"""
        return self.page.text_content(locator)

    def title(self):
        """获取页面标题"""
        return self.page.title()
```

### tests/test_home.py

```python
"""示例测试用例"""

import allure
from pages.base_page import BasePage


@allure.feature("首页")
class TestHome:
    @allure.story("打开首页")
    @allure.title("验证去哪儿网首页可正常打开")
    def test_open_home(self, page, base_url):
        home = BasePage(page)
        with allure.step("打开首页"):
            home.open(base_url)
        with allure.step("断言页面标题"):
            assert "去哪儿" in home.title()
```

### pages/__init__.py / tests/__init__.py / config/__init__.py / utils/__init__.py

均为空文件，用于标记 Python 包。

### utils/logger.py（可选）

```python
"""日志工具（可选）"""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_logger(name):
    return logging.getLogger(name)
```

## 注意事项

- 浏览器使用 `channel="chrome"` 调用系统安装的 Chrome，不需要执行 `playwright install` 下载浏览器内核。
- 若用户已有 `.venv` 虚拟环境，生成后提示使用 `.venv\Scripts\python.exe -m pip install -r web-demo/requirements.txt` 安装依赖。
- 生成前若 `web-demo/` 已存在，先询问用户是覆盖还是合并，避免覆盖已有代码。
- 用户指定了被测站点或结构偏好时，以用户要求为准，本模板仅作默认参考。