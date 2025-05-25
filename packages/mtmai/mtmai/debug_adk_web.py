#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from google.adk.cli import main

if __name__ == "__main__":
  # 设置当前工作目录为agents目录
  agents_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")
  os.chdir(agents_dir)

  # 设置命令行参数，相当于执行 adk web .
  sys.argv = ["adk", "web", ".", "--port", "7877"]

  # 执行ADK CLI的main函数
  sys.exit(main())
