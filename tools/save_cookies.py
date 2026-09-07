"""Cookie 登录态复用：一次性手动登录生成 cookie 文件，供 conftest 注入，绕过短信验证码

用法（两种均可）：
  python web-demo/tools/save_cookies.py
  或 在 web-demo 目录下 python tools/save_cookies.py

流程：打开去哪儿统一登录页（含扫码登录）→ 用户扫码/登录 → 脚本自动检测登录成功 → 访问机票页种 Cookie → 保存 cookies.json
"""
import json
import sys
import time
from pathlib import Path

# 支持直接运行：将 web-demo 目录加入 python 搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright  # noqa: E402

from paths_manager import COOKIE_FILE  # noqa: E402

# 统一登录页（手机扫码/密码登录均可），登录成功后跳回 www.qunar.com
LOGIN_URL = "https://user.qunar.com/passport/login.jsp?ret=https%3A%2F%2Fwww.qunar.com%2F"


def save_cookies():
    """打开登录页并等待用户登录（扫码即可），自动检测成功后保存 storage_state"""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context(locale="zh-CN")
        page = context.new_page()
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("请在浏览器中完成登录（推荐扫码），登录成功后脚本将自动继续并保存 Cookie...")

        # 自动检测登录成功：passport 登录页会在登录后跳离 login.jsp
        deadline = time.time() + 300
        while time.time() < deadline:
            page.wait_for_timeout(2000)
            if "login.jsp" not in page.url:
                break
        else:
            raise TimeoutError("等待登录超时（5 分钟），请重新运行")

        print("登录成功，访问机票页并保存登录态...")
        # 登录后再访问机票页，确保 flight 域相关 Cookie 已种下，供航班列表/预订流程使用
        page.goto("https://flight.qunar.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        state = context.storage_state()
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"登录态已保存到 {COOKIE_FILE}")
        browser.close()


if __name__ == "__main__":
    save_cookies()
