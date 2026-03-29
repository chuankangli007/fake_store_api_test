# Fake Store API 接口自动化测试项目
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-7.4.2-green.svg)
![Requests](https://img.shields.io/badge/Requests-2.31.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 项目背景
这是一个**接口自动化测试实战项目**，基于 Fake Store API（开源电商测试接口）实现核心电商流程测试。  
作者作为大一Python学习者，通过该项目掌握「接口请求封装、测试用例设计、Pytest夹具复用」等基础能力，模拟真实电商场景的测试逻辑。

## 核心亮点
✅ **使用基本的pytest框架**：无复杂框架依赖，仅使用Python内置库+Pytest+Requests   
✅ **贴近实战**：模拟「登录鉴权→购物车操作」的真实电商流程，体现测试思维  
✅ **代码规范**：模块化封装、清晰注释、日志输出，符合自动化测试基础规范  
✅ **结果可视**：终端直接输出测试结果，无需额外报告工具，但是可以下载pytest-html
第三方库，生成HTML测试报告，作者最后自己生成了html报告。

## 项目介绍
 **项目采用‘正向+负向’结合的用例设计思路，确保覆盖全面**：正向设计合理的用例成功创建商品，注册用户，创建购物车等，负向使用错误的价格和邮箱

 **项目细节**：分布了11个测试点，12个测试用例,最后通过测试用例10个，预期失败测试点2个

 **关键问题**：  
 1.向Fake Store API访问一个不存在的id，不会按常理返回404，而是会返回200状态码，
 并且和一个空的数据因为无法解析为json格式，所以会触发ValueError错误  
 2.Fake Store API在面对一个负数价格的商品的创建的时候，会返回201状态码，而不是常规的400类的状态码  
 3.Fake Store API无法对已经注册的账号进行记忆，所以无法用正确验证注册的账号进行登录获取token，只能用官方给的账号进行登录，并且还不会返回id

 **解决办法**：  
 1.在封装get请求的时候使用try—expect将预期的ValueError错误进行处理  
 2.使用@pytest.mark.xfail标记，预计错误，区分已知的API缺陷和新发现的Bug  
 3.对于无法放回id，采用直接给通过合法id模拟这个功能,使这个功能能正常测试。



## 快速开始
### 1. 环境要求
- Python 3.8+（推荐3.9）（作者本人使用的是python3.12）
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