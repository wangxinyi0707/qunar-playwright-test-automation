"""项目路径常量：统一管理各目录与文件的绝对路径"""
from pathlib import Path

# 项目根目录（web-demo/）
ROOT_DIR = Path(__file__).resolve().parent

# 各子目录
ACTIONS_DIR = ROOT_DIR / "actions"
COMMON_DIR = ROOT_DIR / "common"
PAGES_DIR = ROOT_DIR / "pages"
CONFIG_DIR = ROOT_DIR / "config"
TESTCASES_DIR = ROOT_DIR / "testcases"
TOOLS_DIR = ROOT_DIR / "tools"
LOGS_DIR = ROOT_DIR / "logs"
IMAGES_DIR = ROOT_DIR / "images"
REPORTS_DIR = ROOT_DIR / "reports"

# 常用文件路径
LOG_FILE = LOGS_DIR / "test.log"
COOKIE_FILE = ROOT_DIR / "cookies.json"

# 运行时目录不存在则自动创建
for _dir in (LOGS_DIR, IMAGES_DIR, REPORTS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)
