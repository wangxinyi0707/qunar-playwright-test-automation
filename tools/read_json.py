"""纯工具：读取 config 目录下的 json 测试数据"""
import json
import sys
from pathlib import Path

# 支持直接运行：将 web-demo 目录加入 python 搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from paths_manager import CONFIG_DIR  # noqa: E402


def read_json(filename: str) -> list:
    """读取 config 目录下的 json 文件，返回数据列表"""
    path = CONFIG_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)
