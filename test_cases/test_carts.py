import pytest
import yaml
from utils.http_request import http_request
from utils.logger import log

with open("./config/test_data.yaml", "r", encoding="utf-8") as f:
    test_data = yaml.safe_load(f)


class TestCarts:
    # -------------- 测试1：创建购物车（下单，正常场景）--------------
    def test_create_cart_valid(self,init_env,login_user_token):
     """测试点：登录后创建购物车，模拟下单流程"""
     #演示登录token的使用（Fake Store API不校验，仅体现逻辑）
     http_request.headers['Authorization']=f'Bearer {login_user_token}'
     #因为Fake Store API的功能问题，使用官方给的账号可以登录但是不会放回id，所以我这里会直接给个id
     user_id=1 #模拟登录用户的ID
     cart_data=test_data['cart']['create_valid']
     cart_data['userId']=user_id

     response=http_request.post('/carts',json_data=cart_data)
     result=response.json()

     assert response.status_code==201,'创建购物车失败'
     assert 'id' in result,'未返回购物车ID'
     assert len(result['products'])==len(cart_data['products']),'商品数量不一致'
     log.info(f"下单成功，购物车ID：{result['id']}，用户：{user_id}，使用登录token：{login_user_token[:6]}...")


    # -------------- 测试2：查询所有购物车（正常场景）--------------
    def test_get_all_carts(self,init_env):
        """测试点：查询所有购物车，验证返回列表非空"""
        response=http_request.get('/carts')
        result=response.json()

        assert response.status_code == 200, "查询失败"
        assert isinstance(result, list), "返回数据不是列表"
        assert len(result) > 0, "购物车列表为空"
        log.info(f"查询所有购物车成功，共{len(result)}个")




