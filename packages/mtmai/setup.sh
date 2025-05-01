#!/usr/bin/env bash

uv pip install crawl4ai --no-deps


function setup_mtmai_dev() {

  uv sync
  # 原因: crawl4ai 库本本项目有冲突,所以使用独立的方式设置
    uv pip install crawl4ai f2 --no-deps

    # 原因: moviepy 库 引用了  pillow <=11
    uv pip install moviepy>=2.1.2 --no-deps

    uv add playwright_stealth

}

setup_mtmai_dev
