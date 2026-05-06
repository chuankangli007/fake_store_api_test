import sys
from pathlib import Path
# 将项目根目录添加到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))


import pytest
import yaml
from utils.http_request import http_request
from utils.logger import log

#读取测试数据，避免重复
with open('./config/test_data.yaml','r',encoding='utf-8') as f:
    test_data=yaml.safe_load(f)

    #-----------夹具 1：初始化测试环境---------------
@pytest.fixture(scope='session')
def init_env():
    """会话级夹具：验证接口是否可用（所有用例执行前运行一次）
    Fixture 是 pytest 的核心功能，
    用来封装测试用例的前置 / 后置操作（比如初始化环境、创建测试数据、清理资源），
    测试用例可以直接 “依赖” 这些夹具，不用重复写相同代码。"""
    log.info('===初始化测试环境===')
    try:
        response=http_request.get('/products/1')
        assert response.status_code == 200,'接口不可用'
        log.info('===初始化环境测试成功')
    except Exception as e:
        log.error(f'测试环境初始化失败；{str(e)}')
        raise
    yield
     #--------夹具2：创建测试商品用例（供更新删除用例）
@pytest.fixture(scope='module')#scope='module'表示每个.py文件运行隐藏这个夹具
def create_test_product():
    create_data=test_data['product_create']['valid_data']
    response=http_request.post('/products',json_data=create_data)
    product_id=response.json()['id']
    log.info(f'创建测试用例成功，ID：{product_id}')

    #传递商品id给用例
    yield product_id

    #用例执行完，删除商品（清理数据）
    http_request.delete(f'/products/{product_id}')
    log.info(f'商品删除成功，id：{product_id}')

    #---------夹具3：用户登录获取token(供购物车)--------
@pytest.fixture(scope='module')
def login_user_token():
    """模块级夹具：用户登录→获取token→用例使用"""
    log.info(f'===用户登录获取token===')
    login_data=test_data['user']['login_valid']
    response=http_request.post('/auth/login',json_data=login_data)
    token=response.json()['token']
    log.info('用户登录成功，已经获取token')

    yield token

    log.info('===登录状态无需清理===')










