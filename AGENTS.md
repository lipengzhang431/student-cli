# 项目执行标准

## Python 环境

- 一律使用项目根目录下的虚拟环境：`.venv/`
  - 运行脚本：`.venv/Scripts/python.exe <脚本>`（Windows / Git Bash）
  - 安装依赖：`.venv/Scripts/python.exe -m pip install <包名>`
- 不要使用系统全局 Python，不要新建其他虚拟环境。

## 练习代码组织

- 每天的练习写进独立的 `dayN.py`（如 `day4.py`、`day5.py`），不要堆在 `main.py` 里。
- `main.py` 保留为早期的综合演示文件，不追加新的按天练习。

## 测试规范

- 测试框架使用 **pytest**。
- 测试文件统一存放在 `tests/` 目录。
- 当天的测试统一写进当天的测试文件：`test_dayN.py`（如 `day4.py` 的测试写在 `tests/test_day4.py`）。
- 运行方式：`.venv/Scripts/python.exe -m pytest tests/ -v`

## 历史说明

- `tests/test_day3.py`、`tests/test_day4.py` 现为 unittest 风格，是 pytest 完全兼容的写法，可继续运行；新增测试直接按 pytest 风格编写即可。
