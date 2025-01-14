import os
import platform
import sys
from pathlib import Path


def in_jupyter_notebook():
    return "JPY_PARENT_PID" in os.environ


def is_in_docker():
    return Path("/.dockerenv").exists()


def is_ubuntu():
    if platform.system() != "Linux":
        return False
    try:
        with open("/etc/os-release") as f:  # noqa: PTH123
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"').lower() == "ubuntu"
    except FileNotFoundError:
        return False
    return False


def is_in_huggingface():
    return os.getenv("SPACE_HOST")


def is_in_vercel() -> bool:
    return os.getenv("VERCEL") == "1"


def is_in_temboio():
    return os.getenv("VISUALLY_MEASURED_DOWITCHER_TMPBOAI_PORT")


def is_in_windows() -> bool:
    return platform.system() == "Windows"


def is_in_testing() -> bool:
    """是否处于测试环境"""
    return "pytest" in sys.modules or os.getenv("PYTEST_CURRENT_TEST")


def init_env():
    sys.path.insert(0, str(Path("./mtmlib").absolute()))
    sys.path.insert(0, str(Path("./mtmtrain").absolute()))
