"""一键跑测试 + 生成 Allure 报告

用法：在 web-demo 目录下执行  python run.py
"""
import os
import subprocess
import sys

import pytest

from paths_manager import REPORTS_DIR, ROOT_DIR


def run_tests() -> int:
    """执行全部测试，收集 allure 结果"""
    os.chdir(ROOT_DIR)
    exit_code = pytest.main([])
    return exit_code


def generate_report():
    """生成并打开 Allure 报告（需先安装 allure 命令行工具）"""
    results = REPORTS_DIR / "allure-results"
    report = REPORTS_DIR / "allure-report"
    subprocess.run(
        ["allure", "generate", str(results), "-o", str(report), "--clean"],
        check=True,
    )
    subprocess.run(["allure", "open", str(report)], check=True)


if __name__ == "__main__":
    code = run_tests()
    if code != 0:
        sys.exit(code)
    generate_report()
