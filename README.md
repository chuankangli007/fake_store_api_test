# Fake Store API 接口自动化测试项目
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-7.4.2-green.svg)
![Requests](https://img.shields.io/badge/Requests-2.31.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 项目背景
这是一个**面向入门级开发者的接口自动化测试实战项目**，基于 Fake Store API（开源电商测试接口）实现核心电商流程测试。  
作为大一Python学习者，通过该项目掌握「接口请求封装、测试用例设计、Pytest夹具复用」等基础能力，模拟真实电商场景的测试逻辑。

## 核心亮点
✅ **零基础友好**：无复杂框架依赖，仅使用Python内置库+Pytest+Requests 
✅ **贴近实战**：模拟「登录鉴权→购物车操作」的真实电商流程，体现测试思维  
✅ **代码规范**：模块化封装、清晰注释、日志输出，符合自动化测试基础规范  
✅ **结果可视**：终端直接输出测试结果，无需额外报告工具

## 快速开始
### 1. 环境要求
- Python 3.8+（推荐3.9）
- Git（可选，也可直接下载压缩包）

### 2. 安装与运行
```bash
# 克隆仓库
git clone https://github.com/你的GitHub用户名/fake-store-api-test.git
cd fake-store-api-test

# 安装依赖（仅2个核心依赖）
pip install -r requirements.txt

# 运行所有测试用例
pytest

# 运行指定用例（带详细日志）
pytest test_cart.py -v -s